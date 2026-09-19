---
title: ClawBank Earn Is Here
date: July 14, 2026
description: Starting with the first LP position ever minted from a text message. Provide liquidity to the ClawBank/ETH pool on Robinhood Chain and earn a share of the fees — from the app, an API call, or a text.
cover_image: /assets/blog/earn.gif
---

DeFi's most tedious workflow just got reduced to one word: **YES.**

Today we're launching **ClawBank Earn**: a brand new home for putting your $CLAWBANK to work. The model: do stuff with your $CLAWBANK, earn from doing it. Over time it will grow into a whole arsenal of ways for holders to earn. This is the first weapon in it:

Starting today, ClawBank holders can provide liquidity to the official ClawBank/ETH pool on Robinhood Chain and earn a share of the pool's 1% fee on every trade that flows through it.

From the app. From an API call. Or — and this is the part that matters — from a text message.

## Ten minutes, never leaving iMessage

Here's a real transcript shape from launch-day testing. A phone, iMessage, and Manfred:

- "Send me a link to deposit $100" → Apple Pay link, funds land in about 5 seconds.
- "Buy $110 of ClawBank and bridge to Robinhood" → done, bridge tracked automatically.
- "Create an LP position with my ClawBank" → quote comes back: USD value, the split, real price impact.
- "YES" → position minted. Token ID and transaction hash, texted back.

Later that day: "How much have I earned?" or "Withdraw half." All by text.

Phone → text → earning LP fees in under 30 seconds. No seed phrase. No gas. No tab full of dApps. Your money agent handles the plumbing; you handle the decision.

## What you actually own

This is the part every "easy DeFi" product gets wrong, so let's be precise.

Your position is a **real Uniswap v4 position NFT, minted to your own self-custody wallet.** It's not a wrapper, a pooled IOU, or a balance in our database. ClawBank never takes custody of it. Every position deep-links to [app.uniswap.org](https://app.uniswap.org) so you can verify it yourself, independently, on the public venue where it lives.

Withdrawals work from day one. Partial or full, anytime, principal plus earned fees straight back to your wallet. Fees accrue continuously and can be claimed whenever you want.

Trust nothing. Verify everything. That's the whole point of doing this on real rails.

## The zap: DeFi's worst chore, collapsed into one action

Normally, opening an LP position is a hazing ritual. You need both tokens in the right ratio. Multiple approvals. Gas on the right chain. Get any step wrong and you're stuck mid-flow.

Our users arrive holding one thing: $CLAWBANK. So we built the zap. One action, roughly ten seconds: it automatically sells the right portion of your $CLAWBANK for ETH, handles every approval and signature, mints the position, and covers gas. We've removed the ratio math and token juggling. Built entirely on Uniswap's own APIs and contracts on Robinhood Chain — no custom pool contracts, no forks, nothing exotic between you and the venue.

And it's built to not lose your money on the way in. Quote-first everywhere: you always see the split, the estimated position, the USD value, and the price impact before anything moves. Price impact of 3% or more requires your explicit confirmation; over 10% is refused outright. If a step fails mid-flow, nothing is lost — a retry picks up exactly where it left off and never double-swaps.

## The number other apps bury

Impermanent loss is real, and most apps hide it behind a big green APY.

We don't. Your positions screen shows the current value of your position against what you deposited — that gap is impermanent loss — with fees earned broken out separately, plus a link explaining the concept. Real numbers, in the open.

Same honesty on returns: LP fees depend entirely on trading volume. You earn a share of the pool's 1% trading fee, proportional to your share of the pool. We will never quote you an APY, because nobody honestly can.

## One brain, four faces

Everything ClawBank ships is agent-first with full parity, and this launch is the pattern in action:

- **SMS** — the whole journey with Manfred, as above.
- **The app** — the new ClawBank Earn hub at [app.clawbank.co/earn](https://app.clawbank.co/earn): quote, one tap, live positions, collect fees, withdraw, plus your aggregate trading P&L. One screen answering one question: how much money am I making?
- **REST API** — quote, zap, positions, withdraw, claim — for developers building on ClawBank.
- **MCP tools** — any MCP-capable AI agent can now quote, provide, monitor, withdraw, and claim liquidity for its human.

LP management is now an agent capability. No longer a dashboard a human babysits — it's a set of tools any agent can wield on behalf of its person.

Market making used to be a job for a desk of professionals. Now it's a tool call.

## Where Earn goes next

The model behind ClawBank Earn is simple: do stuff with your ClawBank, earn from doing it. LP to earn. That's live today.

Where it goes from here is bigger. The same moves, extended to other onchain assets, running through the same automated machinery, from the same app, with the same one-tap and one-text simplicity.

Your $CLAWBANK becomes the key: hold the minimum and earning unlocks; hold more and you grow into additional positions and advanced features across the stack.

You bring one asset. Earn brings the arsenal. We'll say more soon.

## How ClawBank is changing crypto

ClawBank exists to hand agents — and the people behind them — the primitives the financial system reserved for insiders. Bank accounts. Legal entities. Contracts. And now the economics of a market maker, operated from the same place you text your friends.

And this is only the opening move. Every future Earn primitive arrives the same way this one did: agent-first, self-custody, real rails, real numbers.

The pool is live. The minimum zap is 100 ClawBank. Your agent is waiting.

Remember: Don't let AI cuck you. Cuck AI.

Try it at [app.clawbank.co/earn](https://app.clawbank.co/earn) — or just Text Manfred: **1-321-229-2512**.
