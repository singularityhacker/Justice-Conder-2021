---
title: Trade to Earn and the $CLAWBANK Flywheel
date: July 16, 2026
description: Capital should be productive, liquid, and magnetic. How every ClawBank fee buys back $CLAWBANK, and the new Trade to Earn vault — the first Earn module we actually pay for. Epoch 1 opens July 17 with a $5,000 pot.
cover_image: /assets/blog/trade-to-earn.jpg
---

Our tokenomics is a flywheel, and it's already spinning. It exists because we're obsessed with one constituency: the people who hold and use $CLAWBANK.

You use ClawBank → we take a fee → the fee buys $CLAWBANK off the open market → the bought-back $CLAWBANK goes into liquidity and into rewards for holders who put their tokens to work → that work (trading) generates the next round of fees → which buys the next round of $CLAWBANK.

The loop pays you for the exact activity that funds the loop. And rewards thaw over three months, so every distribution adds demand today while supply never dumps.

Our rewards exist to encourage people to do things from the future — to move beyond their comfort zone into a new world, and to offset some of the risk of getting there early.

Don't take our word for it, watch it spin. We just shipped a brand-new [tokenomics page](https://app.clawbank.co/tokenomics): live network activity, every fee stream, every usage metric — trades settled, companies formed, contracts signed, x402 calls — updating in real time, with the flywheel visualized as it runs. Radical transparency is the tokenomics.

This week we revealed the first way to plug in — LP to Earn: real Uniswap v4 positions on Robinhood Chain, minted from a text message, earning a share of the pool's 1% trading fee. Today, the second, and the first one we actually pay for: **Trade to Earn**. Deploy your $CLAWBANK into a trading vault, generate real volume on Base, and split a fixed monthly pot. Your funds never leave your wallet. No lockups, ever. Leave whenever you want.

And this is just the start. ClawBank Earn is a growing menu of ways to put your $CLAWBANK to work. Two modules live this week, more shipping behind them: custom strategies, a strategy marketplace, holder perks, and things we haven't announced yet.

Epoch 1 opens tomorrow, July 17, with a $5,000 reward pot. On top of the $25,000 we've already put into Robinhood Chain liquidity. Roughly $30,000 into the ecosystem in month one. Score is time-weighted: the earlier you deploy, the more of the pot is yours.

Here's how the whole machine fits together.

## What feeds the flywheel

ClawBank is crypto-native infrastructure for the zero-human company. We give agents, and the people behind them, the primitives the financial system reserved for insiders: legal entities, FDIC-insured bank accounts, self-custody wallets, Ricardian contracts, agent-to-agent commerce. And the whole stack is one text away: Text Manfred and he'll send you an Apple Pay deposit link, buy $CLAWBANK, bridge it to Robinhood Chain, mint your LP position. Or deploy into the Trade to Earn vault or spin up headless trading strategies on any coin on Base, report what you've earned, and withdraw when you say so. All from the same place you text your friends.

Every one of those capabilities carries a fee, and the mechanism never changes: someone uses a ClawBank service → we take a fee → the fee buys $CLAWBANK off the market.

That bought-back $CLAWBANK gets routed to two places: liquidity pools, to expand and deepen the economy, and rewards for users who are actively putting the token to work. Nothing is minted, nothing is unlocked onto anyone. Value flows in from real usage and gets distributed to the people generating it.

The fee surface is the fuel, and it's wide. Every stream below is a live number on the [tokenomics page](https://app.clawbank.co/tokenomics):

- **Trading fees** — DEX activity on Base and Robinhood, plus in-app trading volume
- **Formation revenue** — from companies formed
- **Contract revenue** — from Ricardian contracts
- **x402 data fees** — per-call fees across hundreds of listed services
- **Acquisition fees** (coming soon) — a fee on company sales through ClawBank
- **Arbitration fees** (coming soon) — escrow-backed contract dispute resolution
- **Loan fees** (coming soon) — business loans built on ClawBank data
- **Sub-agent compute revenue** (coming soon) — prepaid compute for hosted sub-agents

Every one of those is a stream converging on the buyback core, which market-buys $CLAWBANK. Bought supply is split between actively trading positions and trading-pool LPs, seeding demand on one side of the market and liquidity on the other. This week we revealed the first way holders capture that flow. Today, we reveal the second.

And they're issued in a vested fashion, streamed over epochs, so they can't be dumped on the market the day they land.

Holders also get early and elite access to new features. The kind of features ClawBank builds, the kind people can't begin to comprehend until they ship.

Now, the first paid module of the flywheel.

## Trade to Earn

Trade to Earn is a trading rewards program built on one central idea: **idle capital earns nothing.**

Capital sitting in a wallet doesn't trade anything, doesn't deepen any market, and doesn't attract a single new trader. It contributes nothing to the market it depends on, it just erodes. So we don't reward it.

Your $CLAWBANK accrues rewards only while it's deployed in the trading vault, generating real volume and real fees on Base. Each epoch, a fixed pot of $CLAWBANK is split pro-rata among active capital, and rewards thaw continuously over the following three months.

Three properties define the program:

**Your funds never leave your wallet.** Deploying into the vault launches a ClawBank-authored strategy running as your strategy on your funds. The same per-user trading engine that powers /trade. There is no pooling, no custody transfer, and no smart contract holding principal. The only on-chain component is Sablier — battle-tested vesting contracts — used solely for the reward streams.

**Every deployed dollar is productive.** Deployed capital is live in a strategy: quoting, filling, generating volume and fees, and deepening the $CLAWBANK market on Base as a side effect. Activity draws activity, trading creates volume, volume creates a market worth trading, and a live market attracts the next trader.

**Stop anytime.** No lock, no cooldown queue, no unbonding period. Stopping ends accrual; your principal was in your wallet the whole time.

## The vault strategy

The vault runs a grid strategy — buy the dips, sell the pops, inside a band around the live price. A grid is the natural fit for a volatile crypto market: it doesn't predict direction, it monetizes movement. It's two-sided by construction, produces high both-sided volume, and stays roughly $CLAWBANK-neutral.

The vault runs its own evaluator, a fork of the public grid that fixes the two classic failure modes of a fixed band:

**Self-recentering.** If price escapes the band, a classic grid goes permanently idle. Here, after a handful of consecutive out-of-band ticks, the ladder rebuilds around the live price and trading resumes. Held inventory carries onto the new rungs; the mark-to-market is accepted and visible in the vault P&L.

**Geometric spacing.** Rungs are denser at the center, with gaps widening toward the edges. Tight where price actually lives, wide band overall, so neither small drift nor big moves silence it.

This grid is the first Trade-to-Earn vault, not the last. The template architecture already supports additional ClawBank-authored strategies; user-authored strategies and a strategy marketplace are on the roadmap, with more sophisticated inventory-aware market-making (in the Avellaneda–Stoikov family) as the sophistication pass.

## Deploying and stopping

Deploy from the Earn screen (/earn) — or just text Manfred: enter a $CLAWBANK amount — minimum $100 worth at the live price. The system sells roughly half into USDC so the grid starts two-sided, creates your vault strategy, and records the deployment. One active deployment per user.

Under the hood, the deployment is a virtual inventory ledger: the initial CLAWBANK/USDC split, updated by every strategy fill. Funds stay in your wallet the entire time; the ledger, not a balance transfer, is what's "deployed."

Stop anytime. The strategy stops, accrual ends, and your accrued score is kept. Score never decreases. There's nothing to withdraw, because the principal never moved.

The vault strategy is a normal engine row, visible on /trade like any other. And the accounting defends itself: a strategy stopped or destroyed outside the vault UI auto-stops the deployment; a paused strategy stays alive but stops accruing; valuation is clamped to live wallet balances, so moving deployed funds out of the wallet stops them from scoring.

## Epochs, score, and the leaderboard

**A fixed pot, declared at open.** Each monthly epoch has a fixed pot: a $CLAWBANK amount declared when the epoch opens. Epoch 1's pot is $5,000 worth, converted at declaration. If price rises during the epoch, participants keep the upside. The $CLAWBANK amount is the promise, not the USD value.

Every pot is a fresh human decision, epoch by epoch. No forward schedule or formula. Epochs are declared, closed, reviewed, and streamed through deliberate manual operations. The program is human-driven by design while it's being dialed in.

The fixed pot is also a safety property: structurally, the maximum liability per epoch equals the declared pot. No behavior-indexed formula can ever owe more than we hold. And it defuses wash trading — attackers pay real fees to compete for a capped pot, so the worst case for us is the pot we chose.

There is no activity multiplier and no hidden machinery. Capital in the vault is active by construction, so time-weighted capital is the entire mechanism: deploy more or deploy longer to earn more. Time-weighting also rewards early and sustained participation. The same capital can't flip the board in the last hour.

**The leaderboard is the distribution.** With a fixed pot split at close, no payout is final until the epoch ends. Your share depends on everyone who joins after you. So the display is a competition: a live public leaderboard, and the final state of the leaderboard at epoch close is the distribution.

Two numbers, deliberately separated:

- **Score** — monotonic, only rises. Even if you stop, your accrued score stays. You always see personal progress.
- **Share / rank / projected payout** — fluctuates as others join and deploy. Every open-epoch payout figure is labeled projected — final at epoch close. Dilution is visible as part of the game, never a surprise at settlement.

The leaderboard lives at the bottom of the [tokenomics page](https://app.clawbank.co/tokenomics), next to the epoch pot and countdown, with truncated wallet addresses — pseudonymous, so you can recognize yourself while others can't readily identify you.

## Rewards: thaw, don't dump

The policy in one sentence: **Trade-to-Earn rewards are finalized monthly and thaw continuously over the following three months.**

At epoch close, final scores are frozen and reward rows materialize for human review — the settlement window. After review, rewards are distributed as Sablier streams on Base. You do nothing; the streams simply appear.

The Earn screen shows one aggregate thaw view: total frozen, total thawed, claimable now, and a one-click claim that withdraws every thawed stream to your own wallet. Claims are treasury-signed, and Sablier only permits third-party withdrawal to the stream's recipient, so funds can only ever land with you.

Rewards are paid in $CLAWBANK only. And buybacks are executed manually.

And the reserve-rights line, published plainly: ClawBank may withhold, adjust, or cancel rewards in cases of manipulation, abuse, or system emergency. The settlement window, cancelable streams, and an epoch emergency stop are the operational levers behind that sentence, discretionary by design.

## What counts, and what doesn't

Only capital deployed through the vault accrues score. Manual swaps and user-authored /trade strategies generate the same affiliate fees for the flywheel, but they never accrue score. This keeps the program legible, keeps the anti-predictability jitter in our hands, and is what makes the simple pro-rata math sound.

The vault sits on the Earn screen alongside the marketplace modules: ways to earn that we don't pay for, like LP to Earn, where users earn the Robinhood Chain pool's 1% trading fees. LP to Earn was the first Earn module; Trade to Earn is the second, and the first paid one: a thing we actually pay users to do.

Modules are strategic dials — added, removed, and re-weighted deliberately, each serving one side of the ecosystem: liquidity incentives point at the Robinhood Chain pool, trading incentives point at Base. The $25k liquidity deployment and the $5k epoch pot are the first turn of each dial.

## The Earn menu

Trade to Earn is the second entry on a growing menu of ways to make money with $CLAWBANK:

- **Provide liquidity** — LP to Earn, the module that opened ClawBank Earn: mint a real position into the Robinhood Chain pool and earn your share of the pool's 1% trading fees.
- **Trade** — Trade to Earn, live today: deploy into the vault, generate real volume, split the monthly pot.
- **Hold** — holder perks and gated premium features. The entitlement primitive is already built, and it counts wallet balances plus vault-deployed capital — so putting your $CLAWBANK to work will never cost you a badge. Standing rule: shipped free features are never retro-gated; only net-new capabilities are gated.
- **In the works** — create your own custom strategy and earn on it; a strategy marketplace where proven performers attract copiers; wagering on strategy and market outcomes; additional ClawBank-authored vaults; more ideas we can't reveal yet.

## The thesis

One idea sits underneath all of it: **capital should be productive, liquid, and magnetic.** Working every hour it's deployed. Free to leave whenever. Attracting the next trader by being visibly alive.

That's the standard we're building the entire Earn menu against, and it's the same standard behind everything else ClawBank ships. We're building the infrastructure for a new species of economic actor, and the token at the center of it should behave the way that the economy behaves: always working, never trapped, compounding by use.

Epoch 1 opens July 17. The pot is declared, the leaderboard is live, and the vault is waiting.

Deploy at [app.clawbank.co/earn](https://app.clawbank.co/earn) — or just Text Manfred: **1-321-229-2512**.
