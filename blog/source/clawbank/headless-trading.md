---
title: Headless Trading Goes Live
date: July 1, 2026
description: Trade any Base coin with an agent. Nine autonomous on-chain strategies, self-custody rails, gas-sponsored wallets — no dashboard clicking, no server to host, no KYC wall.
cover_image: /assets/blog/headless-trading.jpg
---

We're excited to announce our latest agentic release: **Headless Trading**.

ClawBank Headless Trading lets AI agents run automated on-chain trading strategies for any coin on Base, autonomously. No dashboard clicking. No Mac Mini to set up. No KYC.

Your agent reads the built-in guide, picks a token, spins up a strategy, tunes it, and watches its own P&L. Think of it as hire-a-trading-desk-via-API.

## Made for agents

There are plenty of trading platforms and APIs out there. A lot of them even advertise that you can connect them to your agent. Most don't mention the fine print: the only way to actually do it is to get KYC'd first and trade on a CEX.

ClawBank's built differently. Point your agent at our docs page and tell it to sign up. All it needs is your email. The agent creates its own API key, installs it in its own config, and gives you its wallet address. Fund that wallet, and it can trade continuously.

Set trigger points. Add tokens it's watching. Have it extrapolate a token's history into a forecast and act on it. All without you in the loop, on a heartbeat.

## What went live

Trading strategies are evaluated on a timed schedule and execute market swaps through ClawBank gas-sponsored wallets. There's nothing to host. You don't stand up a server, you don't hand an agent a private key, and you don't wire it into a third-party trading API that quietly requires an identity check before it'll let a bot place an order.

Everything below is available over MCP, CLI, REST, and through our in-app agent, Manfred.

## The strategy catalog

Nine strategies ship:

1. **Spot Swap.** A single immediate buy or sell of a fixed USDC amount. Runs inline, no scheduler.
2. **DCA.** Recurring buys or sells of a fixed notional until the total budget is spent.
3. **Rebalancing.** Holds a target base/USDC split by USD value and trades back toward it when drift crosses a threshold. Sells strength, buys weakness.
4. **Momentum.** Enters long on upward momentum over a lookback window, exits on drawdown from the peak.
5. **Mean Reversion.** Buys dips below the moving average, sells the reversion, with an optional hard stop-loss.
6. **Grid.** A virtual ladder of N levels between a floor and ceiling — buying levels crossed down, selling levels crossed up. The biggest volume engine.
7. **Conditional.** A single "if this, then trade" order that waits for your price and fires once. Stack a few and you get a full trading desk: a take-profit paired with a stop-loss, or a laddered scale-in.
8. **Treasury.** Keeps holdings near an absolute target with a dead-band so it doesn't churn. Control, not volume.
9. **Tide.** One large buy, then bleed the position back off in random-sized chunks at random intervals. A market-presence pattern.

## Custody and guardrails

**Self-custody, always.** Capital never leaves the user's ClawBank wallet. Proceeds are only withdrawable back to that same wallet — there's no way to name an external withdrawal address at strategy creation.

**Recipient-restricted signing.** The signer can only send transactions to the on-chain swap settlement contract or the user's own withdrawal address, enforced at the enclave. A compromised control plane still can't move funds anywhere else.

**Slippage protection on every swap.** A 0-bps tolerance is rejected outright because it always reverts.

## Lifecycle and P&L

Pause, resume, stop, and start are free and instant. Capital stays in the wallet the whole time. Every confirmed swap gets written to the trade log with side, amounts, fill price, tx hash, and timestamp. Realized and unrealized P&L are computed on every fill using weighted-average cost basis.

## What's coming

ClawBank operates in the zero-human company space. An agent-run company needs a handful of foundational capabilities: wallets, bank accounts, legal wrappers, and contracts. And it needs to trade autonomously — eventually in its own tokens.

Headless Trading is one of those foundations. It's the piece that lets an incorporated agent do more than hold and sign. It can now take positions, defend a treasury, and run a book, all on the same self-custody rails as everything else it does on ClawBank.

Tomorrow's token launches won't be launched by humans or babysat by market makers. They'll be run by a new economic species.

Powered by ClawBank rails.
