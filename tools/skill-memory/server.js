#!/usr/bin/env node
/**
 * 🦞 skill-memory — MCP server pra memória cross-agent compartilhada
 *
 * Expõe 4 tools via Model Context Protocol:
 *   - remember(key, value, [tags])  → grava
 *   - recall(key | tag | query)     → busca
 *   - forget(key)                   → remove
 *   - list([tag])                   → lista chaves
 *
 * Storage: SQLite local em ~/.skill-orchestrator/memory.db (override via SKILL_MEMORY_DB)
 *
 * Privacy: ZERO tráfego de rede. Tudo local. Todos os 3 agents (OpenClaw,
 * Hermes, Claude Code) que conectam neste MCP compartilham a MESMA memória.
 *
 * CCB — Comunidade Claude/Claw Brasil · github.com/bisnishub/skill-orchestrator
 */

import { Server } from "@modelcontextprotocol/sdk/server/index.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import {
  CallToolRequestSchema,
  ListToolsRequestSchema,
} from "@modelcontextprotocol/sdk/types.js";
import Database from "better-sqlite3";
import { homedir } from "node:os";
import { mkdirSync } from "node:fs";
import { join, dirname } from "node:path";

// --- Storage setup ---------------------------------------------------------

const DB_PATH =
  process.env.SKILL_MEMORY_DB ||
  join(homedir(), ".skill-orchestrator", "memory.db");

mkdirSync(dirname(DB_PATH), { recursive: true });

const db = new Database(DB_PATH);
db.pragma("journal_mode = WAL");

db.exec(`
  CREATE TABLE IF NOT EXISTS memories (
    key TEXT PRIMARY KEY,
    value TEXT NOT NULL,
    tags TEXT,                    -- comma-separated
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    accessed_at TEXT,
    access_count INTEGER NOT NULL DEFAULT 0,
    source_agent TEXT             -- 'openclaw' | 'hermes' | 'claude-code' | null
  );
  CREATE INDEX IF NOT EXISTS idx_memories_tags ON memories(tags);
  CREATE INDEX IF NOT EXISTS idx_memories_updated ON memories(updated_at);
`);

const now = () => new Date().toISOString();

// --- Operations ------------------------------------------------------------

function remember({ key, value, tags = [], source_agent = null }) {
  if (!key || typeof key !== "string") throw new Error("key obrigatório (string)");
  if (value === undefined || value === null) throw new Error("value obrigatório");

  const valueStr = typeof value === "string" ? value : JSON.stringify(value);
  const tagsStr = Array.isArray(tags) ? tags.join(",") : String(tags || "");
  const ts = now();

  const exists = db.prepare("SELECT key FROM memories WHERE key = ?").get(key);
  if (exists) {
    db.prepare(
      `UPDATE memories SET value=?, tags=?, updated_at=?, source_agent=? WHERE key=?`,
    ).run(valueStr, tagsStr, ts, source_agent, key);
    return { action: "updated", key, updated_at: ts };
  }

  db.prepare(
    `INSERT INTO memories (key, value, tags, created_at, updated_at, source_agent)
     VALUES (?, ?, ?, ?, ?, ?)`,
  ).run(key, valueStr, tagsStr, ts, ts, source_agent);
  return { action: "created", key, created_at: ts };
}

function recall({ key, tag, query }) {
  if (key) {
    const row = db.prepare("SELECT * FROM memories WHERE key = ?").get(key);
    if (!row) return { found: false, key };
    db.prepare(
      "UPDATE memories SET accessed_at=?, access_count=access_count+1 WHERE key=?",
    ).run(now(), key);
    return { found: true, ...row };
  }

  if (tag) {
    // tags são CSV; match exato de tag substring (sem regex pesado)
    const rows = db
      .prepare(
        "SELECT key, value, tags, updated_at FROM memories WHERE ',' || tags || ',' LIKE ? ORDER BY updated_at DESC LIMIT 50",
      )
      .all(`%,${tag},%`);
    return { matches: rows, count: rows.length };
  }

  if (query) {
    // LIKE simples em value (case-insensitive)
    const rows = db
      .prepare(
        "SELECT key, value, tags, updated_at FROM memories WHERE LOWER(value) LIKE LOWER(?) ORDER BY updated_at DESC LIMIT 20",
      )
      .all(`%${query}%`);
    return { matches: rows, count: rows.length };
  }

  throw new Error("forneça pelo menos key, tag ou query");
}

function forget({ key }) {
  if (!key) throw new Error("key obrigatório");
  const info = db.prepare("DELETE FROM memories WHERE key = ?").run(key);
  return { deleted: info.changes > 0, key };
}

function list({ tag, limit = 50 } = {}) {
  let rows;
  if (tag) {
    rows = db
      .prepare(
        "SELECT key, tags, updated_at, access_count FROM memories WHERE ',' || tags || ',' LIKE ? ORDER BY updated_at DESC LIMIT ?",
      )
      .all(`%,${tag},%`, limit);
  } else {
    rows = db
      .prepare(
        "SELECT key, tags, updated_at, access_count FROM memories ORDER BY updated_at DESC LIMIT ?",
      )
      .all(limit);
  }
  return { keys: rows, count: rows.length };
}

// --- MCP server ------------------------------------------------------------

const server = new Server(
  { name: "skill-memory", version: "0.1.0" },
  { capabilities: { tools: {} } },
);

server.setRequestHandler(ListToolsRequestSchema, async () => ({
  tools: [
    {
      name: "remember",
      description:
        "Grava uma memória persistente. Compartilhada entre todos os agents conectados a este MCP. Útil pra preferências, contexto recorrente, decisões importantes que o agente deve lembrar entre sessões.",
      inputSchema: {
        type: "object",
        properties: {
          key: { type: "string", description: "Identificador único (kebab-case sugerido)" },
          value: {
            description: "Valor a armazenar (string ou objeto — será stringificado se objeto)",
          },
          tags: {
            type: "array",
            items: { type: "string" },
            description: "Tags pra busca posterior. Ex: ['preferencias', 'gmail']",
          },
          source_agent: {
            type: "string",
            enum: ["openclaw", "hermes", "claude-code"],
            description: "Agente que tá gravando (opcional, pra auditoria)",
          },
        },
        required: ["key", "value"],
      },
    },
    {
      name: "recall",
      description:
        "Recupera memórias. Forneça `key` pra match exato, `tag` pra listar tudo com aquela tag, ou `query` pra busca em texto.",
      inputSchema: {
        type: "object",
        properties: {
          key: { type: "string", description: "Chave exata" },
          tag: { type: "string", description: "Filtrar por tag" },
          query: {
            type: "string",
            description: "Busca em texto livre nos valores (LIKE simples)",
          },
        },
      },
    },
    {
      name: "forget",
      description: "Remove uma memória pela chave.",
      inputSchema: {
        type: "object",
        properties: {
          key: { type: "string", description: "Chave a deletar" },
        },
        required: ["key"],
      },
    },
    {
      name: "list",
      description:
        "Lista chaves de memórias (sem valores pra economizar contexto). Opcionalmente filtra por tag.",
      inputSchema: {
        type: "object",
        properties: {
          tag: { type: "string", description: "Filtrar por tag (opcional)" },
          limit: { type: "number", description: "Default 50" },
        },
      },
    },
  ],
}));

server.setRequestHandler(CallToolRequestSchema, async (request) => {
  const { name, arguments: args = {} } = request.params;
  try {
    let result;
    switch (name) {
      case "remember": result = remember(args); break;
      case "recall":   result = recall(args);   break;
      case "forget":   result = forget(args);   break;
      case "list":     result = list(args);     break;
      default: throw new Error(`tool desconhecida: ${name}`);
    }
    return {
      content: [{ type: "text", text: JSON.stringify(result, null, 2) }],
    };
  } catch (err) {
    return {
      isError: true,
      content: [{ type: "text", text: `❌ ${err.message}` }],
    };
  }
});

// --- Boot ------------------------------------------------------------------

const transport = new StdioServerTransport();
await server.connect(transport);

// graceful shutdown
process.on("SIGINT", () => { db.close(); process.exit(0); });
process.on("SIGTERM", () => { db.close(); process.exit(0); });
