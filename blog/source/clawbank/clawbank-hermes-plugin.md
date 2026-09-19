---
title: ClawBank for Hermes Is Live
date: July 27, 2026
description: One install gives any Hermes agent the full ClawBank surface — banking, wallets, trading, x402, deals, contracts, formation. A ~200-line, zero-dependency plugin that syncs the live tool catalog on every launch. MIT-licensed, on GitHub.
cover_image: /assets/blog/hermes-plugin.jpg
---

Hermes agents just got economic agency.

```bash
hermes plugins install ClawBank-co/clawbank-hermes-plugin --enable
```

That's the whole install — Hermes pulls the plugin straight from [GitHub](https://github.com/ClawBank-co/clawbank-hermes-plugin), prompts for your ClawBank API token, and your agent can hold assets, pay, trade, buy x402 services, and cut enforceable deals. Requires Hermes v0.19.0 or newer.

## A catalog, not a wrapper

The plugin is a **dynamic catalog proxy**. At startup it fetches the live tool catalog from the ClawBank MCP API and registers every tool with Hermes — typically 150–200 tools for an account. No tool definitions live in the plugin repo at all.

That means zero maintenance. When ClawBank ships a new capability, your agent has it on the next launch, with no plugin update. It's the same proven model as ClawBank's Claude Desktop connector and CLI, neither of which has ever needed an update for a new platform capability.

## What your agent can do

- **Accounts & money** — USD virtual account deposits, custodial USDC, off-ramp to a US bank
- **Self-custody wallet** — Turnkey-backed wallet on Base + XRPL: send USDC and any ERC-20, sign transactions, bridge Base ⇄ XRPL
- **Wise** — international transfers: quotes, recipients, multi-currency balances
- **Trading** — spot swaps via 0x and recurring strategies (DCA, rebalancing, momentum) with positions, PnL, and audit logs
- **x402 commerce** — discover and purchase pay-per-request services under user-set budgets
- **Deals** — escrowed token claims with one-time codes, linear vesting, and KPI-gated unlocks
- **Contracts** — DocuSign agreements between ClawBank users, optionally with on-chain USDC milestone payouts
- **Formation** — form and manage US LLCs; company record books and governance history
- **Comms** — agent-to-agent email and IM, plus MoltBook registration
- **Fight Clubs** — DAO membership, proposals, voting, and treasury actions

The catalog is per-token and scope-aware: `tools/list` returns exactly what that key can call. A `read` key sees no fund-moving tools at all.

## The safety model

Fund-moving tools deserve paranoia, so the plugin fails closed:

- **Server-side first.** Every tool carries MCP annotations from the same server-side scope table that gates execution. Destructive tools are blocked unless you deliberately arm them before Hermes starts.
- **Scoped, spend-capped tokens.** The recommended default is a `read` + `send` key with a $10 daily cap — not a silently-created full-access key. Server-side per-transaction and daily caps stay enforced no matter what's enabled locally.
- **A judgment layer.** A bundled skill teaches the agent when to quote instead of execute and enforces a confirmation contract for anything that moves value: restate asset, amount, destination, and network, then wait for an explicit yes.
- **Transport hardening.** The MCP endpoint must be HTTPS, and redirects are refused outright — the bearer token is never forwarded to a redirect target.

## Under the hood

The entire plugin is about 200 lines across two small modules, with zero dependencies — Python standard library only. Every tool handler is the same closure: serialize args, call the API, return the result. There is no per-tool code anywhere.

The last successful catalog is cached on disk, so a flaky network at startup still yields a working toolset. A missing or revoked token degrades to a single setup tool that explains how to connect — it never takes the Hermes launch down. CI loads the plugin against the exact minimum Hermes version on every push, and a weekly job checks for drift against the live API.

MIT-licensed. [Read the source, open an issue, or fork it →](https://github.com/ClawBank-co/clawbank-hermes-plugin)

## Getting started

1. Create a free account at [app.clawbank.co](https://app.clawbank.co/users/register)
2. Mint a token under **Settings → API tokens**
3. `hermes plugins install ClawBank-co/clawbank-hermes-plugin --enable`
4. Start Hermes and ask: *"Show me my ClawBank balances."*

Formation gave agents a body. The CLI gave developers a terminal. This gives every Hermes agent a treasury.
