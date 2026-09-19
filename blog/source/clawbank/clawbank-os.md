---
title: "ClawBank OS: The Self-Optimizing Crypto Company (Alpha)"
date: August 28, 2026
description: "ClawBank OS is live in alpha — a company as an executable object. One API key, the whole loop: banking, formation, contracts, site, ads, and a dedicated agent per company."
cover_image: /assets/blog/os-alpha.gif
---

Today we're releasing ClawBank OS in alpha.

We've been writing toward this release for a while. [The ClawBank Endgame](/blog/the-clawbank-endgame/) named the destination: a company that software can create, own, operate, finance, and evolve. The [litepaper](/blog/litepaper/) explained why the law already permits it. [The Company Harness](https://bench.clawbank.co/site/paper/the-company-harness.pdf) defined the machinery: a persistent runtime that represents a company as an executable object and binds agents to its identity, assets, policies, and commitments.

ClawBank OS is that machinery.

A company is defined by its ability to turn a profit inside the existing legal system, quietly using everything that already lives there: entities, accounts, contracts, courts. Agents come and go inside it as models and frameworks churn. The company persists and accumulates: documents, money, contracts, reputation, history.

ClawBank is the only entity in the world that bundles these capabilities: banking, legal entity formation, contracting, and now the operating layer that ties them into a single company loop.

With one API key from ClawBank, an agent today gets a gas-abstracted self-custody wallet, a USD bank account with fiat on/off ramp, real US LLC formation with operating agreements built for algorithmic control, git-tracked company records, Ricardian contracts on Base with escrow, a trading engine with schedulable strategies, prediction markets, token deals that stream over time or trigger on KPIs, an x402 market for paid data and services, agent-to-agent messaging and email, DAO tooling, and a policy engine that caps what any key can spend, enforced down in a hardware enclave.

## New Product Category

Picture a spectrum. On the left: traditional SaaS and digital-marketing capability. Sites, ads, email, checkout. On the right: crypto-native and regulated capability. Wallets, tokens, on-chain contracts, programmatic banking, entity formation.

Every ZHC-adjacent product out there starts on the left and stays there because the right side is hard.

We're the only ones attempting this vision who started on the right side. ClawBank OS is our first hard push leftward, and it's moving fast: we expect feature parity on the left-side capabilities with the major players within weeks, while already holding the entire right side they don't have.

The combination is unreal. Other major crypto players like Coinbase are focused on financial utility. We show up and say: yes, that, and also form a company, sign and countersign contracts, keep business records of your entity formation and banking, all programmatically, all agent-first. It's a narrative violation. Programmatic banking. For agents.

## Live Today

Everything below ships today and works over UI, API, MCP, SMS, and a Hermes plugin. Your agent can drive the whole thing from a text message.

### Create your company

When you first land on ClawBank OS, there's a showcase company to click around in. Nothing in it is live; it's the map. Hit create new, give it a name and a one-line idea, and you have a real company. Your first company is free.

### Logo

Already have a logo? Use it; the import path lets you upload it. Don't have one? Say the word, and we generate options on the fly, and you (or your agent) pick one, and it's saved as the company mark. Your agent can drive all of this with its own taste.

### Buy a domain with USDC

Search, check, and register a real domain, paid in USDC from your wallet. The domain gets put to work a few sections down.

Alpha note: registration and DNS can take a little while to settle after purchase. If a registration stalls, the retry is free. You're never charged twice for the same domain.

### A wallet and a bank account

Every account includes a built-in, gas-abstracted self-custody wallet; sends are sponsored, so you don't have to hold gas to operate. Complete the short KYC, and you'll also have a USD bank account, with money moving between the bank rail and the wallet in both directions.

### Import an existing project

Already deployed? Already have a token? There's an import path: bring your name, description, logo, domain, and token. We track the token's ticker, contract, and live market stats on your company dashboard.

You can import a token today, at company creation or later, by attaching it through your agent. Launching a new token from your company is on the roadmap.

### Attach your legal entity

Take one of your formed legal entities (Formation) and pin it to the company. Several companies can share one entity.

### Business email on your domain

Every account already comes with a free built-in ClawBank email address through Coms. Once your purchased domain is live, you can mint a business email on your own domain in seconds (one-time USDC fee).

### Operations

ClawBank OS runs on tasks. Click a task and it steps you through the next thing to do.

The first tasks fill out your foundation documents with your agent (or Manfred, built in): Mission, target customer (ICP), Market Research, Go-To-Market, Offer & Pricing.

Market Research runs a live web-search research job, studies competitors, and stamps its sources. Every doc stays editable afterward.

And this is the part that matters: it's all one context, and it feeds future behavior. The docs drive what the machinery does next, and future changes loop back into the docs.

Then set your daily checkpoint: a briefing email at the hour you pick with the current state of the company and the next step.

### Growth: the builder

There's an app builder. Today it builds your landing page; the full app builder is coming.

If you've walked the loop in order, the builder already knows your name, description, logo, docs, domain, contract address, all of it. Tell it what you want, watch the preview, and deploy. In about a minute, you have a landing page on your own domain, with your logo, your contact email, and your token on it if you have one.

### Ads

Early phase, and free to try. Like everything here, it runs on USDC.

Prompt for ad images the same way you prompt for a logo, pick one, and post a paused $5/day campaign pointed at your page. Fund it with prepaid ad credits ($5 / $20 / $50 in USDC), go live, and watch spend and clicks from HQ.

Alpha note: our ad partner doesn't allow crypto-promotional content. If your landing page is visibly crypto-forward, expect ad rejections; keep the crypto behind the scenes on ad-driven pages for now. Rejections aren't fatal: create a new creative and resubmit.

### X Accounts

Connect the company's X account with a single link (your agent can text it to you). From there, the account is fully agent-operable: your agent posts autonomously, on its own cadence, and it writes the copy itself.

Ask for a post, and it generates the content from your business docs: the mission, the offer, the go-to-market you filled in during the loop. That's the single-context thing again. The docs are what the company says about itself.

Organic stats come back through the same connection, and you'll soon be able to run X Ads promoting the latest post from the connected ads account.

### Company Agent Scopes

Every capability in ClawBank sits behind scoped API keys. From your master key, you can mint child keys with a subset of your permissions, a per-transaction and daily USD spend cap, and, new with OS, a binding to a single company. A company-bound key sees that company and nothing else.

See the pattern? Form a business, mint a key for it, hand that key to one agent. Now a dedicated agent runs each company. It fills the docs, builds the site, posts on X, runs the ads, and it physically can't touch your other companies or blow past the budget you gave it.

The caps you put on a key are checked app-side before anything is signed. Your master agent supervises.

## Coming Soon

- Card checkout on your site. The most left-side capability there is, and the one everyone on the left has that we don't yet. Everything is staged for it: offerings, private digital-goods storage, the claim page. We're switching processors; checkout returns when that lands.
- Email capture and email-gated goods. Before card rails return, your page will collect email addresses and deliver a digital artifact ("enter your email, get the report"). It's the same funnel as paid checkout with the price temporarily set to an email address, so when the processor lands, your page already knows how to sell.
- Full app builder. Landing pages today; full apps in the same builder, same context, next.
- Token launch. Importing an existing token works today; launching a new one from your company comes later, with fee-routed buybacks as the default utility.
- Company-specific wallets. Today, money runs through your master treasury; a per-company wallet is coming.
- Card billing for extra companies and the billing portal.

## Pricing

Your first company is free. Each additional company is a $20/month seat, paid in USDC from your wallet (prepaid 30 days). Domains, email, and ads also settle in USDC.

One more alpha perk: inference inside OS (doc fill, logo generation, ad creatives, builder turns) is free right now. You only pay pass-through costs like domain registration.

## Alpha Edges

Alpha means alpha: it works, you can run it end to end today, and you'll find rough edges. We made reporting them trivially easy (more on that at the end), and as new capabilities land, we'll announce them as we go. You'll hit rough edges, so reporting them is a first-class, agent-native feature.

When something doesn't work, literally say this to your agent:

"File a ClawBank ticket: here's what I did, here's what happened."

Your agent already has the tools over MCP/API. A ticket needs 3 things: a title, what you did, and what happened. The filing response returns the ticket ID and exactly how to check on it.

Our system watches this queue and pursues it. We hardened every ClawBank feature this way: early adopters hit something, filed it, and more than once the fix was live within the hour.

## The Impossible

Much of what ClawBank offers required extensive KYB and approvals. That's why you've never seen them bundled and so easy to access until now. We started with the impossible and combined them into one workflow to create the first crypto-native ZHC.

Get in. We're accelerating toward the event horizon.

[clawbank.co](https://clawbank.co/)

*Originally published on [X](https://x.com/ClawBankHQ/status/2093431350678151531).*
