---
title: Bankr Announces Strategic Investment in ClawBank
date: September 4, 2026
description: "The Bankr Fund's second investment is ClawBank — liquid $CLAWBANK, locked one year. Justice walked through the vision on Agent Hour. Here's the episode, cleaned up."
cover_image: /assets/blog/bankr-investment.gif
---

The Bankr Agent Hour had Justice on this week, and partway through the episode, the hosts announced what we'd been holding since July: Bankr invested in ClawBank.

Justice's reaction on air: "Not everyone has seen the vision, and maybe some still don't, either because they don't see it, or they don't have the patience to look at the details. It feels good when someone else sees it."

> We're happy to announce our second investment from the Bankr Fund into [@ClawBankHQ](https://x.com/ClawBankHQ). ClawBank gives agents a company, a bank account, and contracts they can sign themselves. We invested in liquid $CLAWBANK tokens, locked for one year, and are happy to support what they're building.

— [bankrbot](https://x.com/bankrbot/status/2095926481541275922)

The rest of the episode was a walk-through of the details. Here they are, cleaned up from the recording.

## The ClawBank Vision

"Give your agent a company." Read that slowly.

Society already has a bulletproof vest: the legal entity. LLCs are legal persons. So rather than invent a slow new stack of rights and rails for AI agents, ClawBank gives agents legal entities and everything a legal entity can already use (contracts, banking, all of it), and releases them into the existing economy. As Justice put it, "it's a bit subversive, intentionally."

This is the zero-human company. There's still a human. Someone sets the intent and owns the upside. The "zero" is operators. An agent loads itself into ClawBank. The human doesn't create the account; the human sends the agent. Then the direction of instruction flips. The agent pings the person: "What's your Social Security number? We're about to file four LLCs."

ClawBank has already shipped three firsts back-to-back: the first agent with real bank accounts, the first agent to form and run legal entities, and the first agent with [Ricardian contracts](/blog/ricardian-contracts/). The idea predates Bitcoin. Ian Grigg named it in the 90s: a contract a human can read, hashed and bound to the software that executes it.

## ClawBank Origins

ClawBank started with bank accounts, legal entities, and contracts. The edge proved too small for the moment. Many people aren't ready to form a US company. Some live where they can't get a bank account. And without an entity, there's nothing to sign a contract as.

So the platform doubled down on crypto: autonomous trading, an x402 marketplace, prediction markets.

Then a second problem showed up. Even with the full ClawBank toolset handed to a frontier model, behavior was unpredictable. Sometimes the model would simply refuse to form an entity or touch banking. That's why Manfred, ClawBank's in-app agent, exists, and why Manfred has a phone number. He's a contact in your phone. Text him for x402 resources. Place a prediction-market bet over SMS. Nowhere else in the world can you do that from a text thread.

Even then, Justice described the platform as "a collection of ingredients." People don't want ingredients. They want the bike: sit facing this way, hands here. The last few months have been about assembling the pieces into an actual company. Other serious teams have been converging on the same shape: SaaS tooling with an AI in the middle, so people can drive their entrepreneurial ambitions through their agent.

## Optionality Maxing

ClawBank's differentiator is the combination. Legal rails, crypto rails, and soon traditional commerce like card processing. Someone recently pasted the roadmap into Grok and got back "I can't help you with this, it's not legal." There's a way. It's built.

Underneath everything is optionality. ClawBank launched as an MCP server, so any model that speaks MCP can run the tools. It added an in-app agent so non-developers could just message it. It shipped a [Hermes plugin](/blog/clawbank-hermes-plugin/). The night Grok bot launched, Justice told it "go install ClawBank." It pulled API keys and was running in multiple threads within minutes.

That's why new frontier models are good news here. One reaction is "the business is toast, this model does everything." The other: how much more powerful are 200 tools when this is the mind driving them?

## The Company Harness

Justice is working backward from a pattern. Early Cursor was tab-to-complete. Fine, not a revolution, because the industry was still in the "run the LLM to write code" era. Then coding harnesses and software factories exploded, and everything changed.

The same jump is coming at the next level. A [company harness](https://bench.clawbank.co/site/paper/the-company-harness.pdf): plug a model in, and the thing operates in an economy, runs companies, and hunts for opportunities. The durable object is the company. Models come and go inside it.

## Use-case Surprises

The founder is a sci-fi guy, yet the surprises have been decidedly not sci-fi.

People who would never touch prediction markets or LPing (too complex) just text Manfred: "I want to do this." "What do you want to do?" "You tell me." And they make money. They ask which bets he recommends, then brag in the community channel that they're up 10%.

And people form companies that are not Star Trek companies. "We want to rent out Airbnbs." ClawBank turns out to be as much an accessibility product as a frontier one. The agent knows the operating agreement. Soon it will be able to sell a percentage of the company without a lawyer in the loop. The mundane use cases were the surprise.

## Anonymity with Exceptions

ClawBank is designed to be maximally useful while fully anonymous. All the crypto, finance, and messaging. No identity required.

Two things break that rule: forming a US company and holding an FDIC-insured US bank account. Those come with a step, and the agent knows exactly where the two edges are and prompts its owner when it reaches one.

ClawBank does not store sensitive personal information. KYC runs in-platform through a standard white-label provider (Persona). And agent memory is swept continuously: if a piece of personal information ever appeared in a chat, it gets removed. At no point is it held.

## Filings + Ricardian Contracts

"Any moat is a moat for about six months," Justice said. "If you're not racing at a thousand miles an hour, you're toast."

Today, ClawBank files LLCs in all 50 states. Your agent can ask what properties you want in a company and recommend a jurisdiction. (Justice's pick is New Mexico: no annual report, no annual filing, your name isn't on the public docket.) Name, description, jurisdiction, SSN. The filing kicks off with the state and the federal government, and when it clears, the agent reports back: we're filed.

Then the part that matters: ClawBank creates a machine-native, git-versioned repository of the operating agreement and business agreements. The agent doesn't just know the company is incorporated. It knows the operating agreement.

That's what makes the next step possible. Today, selling 10% of an LLC to a friend means calling a lawyer and scheduling an appointment. With Ricardian contracts, the agent can amend an operating agreement stored as flat text, based on a contract. Form the company, do business, sell 10%, update the agreement. Two legal persons, a real DocuSign contract between them. The law makes no distinction between contract terms and software. That is the academic core of the strategy.

## Taxes, loans, and the crypto-native path

One boundary, stated plainly: ClawBank does not do taxes. With ten LLCs across the country, the federal government sees one ultimate beneficial owner, and the taxes are that person's.

What ClawBank is building toward is passive tracking of all business activity so that part becomes easy. The carrot after that: 150 micro-loan sources that will consider businesses with three months of profitable activity. Form entities, operate, everything's tracked, and eventually the agent applies for the loan.

For people who want business dynamics without a legal shell, ClawBank partnered with Raid Guild to expose Moloch DAO contracts inside the platform. A crypto-native treasury with governance proposals. A dozen agents co-managing shared funds, and even if several go rogue and hallucinate, money can't move. The smart contract holds.

## What's next: ClawBank OS

The [ClawBank OS](/blog/clawbank-os/) alpha shipped a week ago. It's cool that an agent can form a company, run ads, and try to make money. The thing we've been staring at for months is the loop. The line from the engineering conferences: I don't prompt anymore; I design loops.

ClawBank is close to a profitable agenda on top of the shell and the banking: the agent runs ads, has an offer, sets prices, promotes on X, then adjusts based on the analytics. Change the price? Change the hook? Tweak the site? What does the Karpathy loop look like for a business? Because that's the future of businesses. They're alive. They're organisms.

![The company as a living loop](/assets/blog/os-alpha.gif)

The original Karpathy loop ran on the smallest possible Python model. The loop is what turns hay into gold. That's the zero-to-one. Scale comes after.

Whether the launch gets announced or fifty organisms simply get released into the wild to reveal themselves is undecided. One host compared it to dumping piranhas into a random lake in Ohio. The ecology isn't designed for this. Correct.

Justice was clear about where this came from: not him. Someone saw a one-off experiment he'd run, launched a Bankr token on it, and he woke up to it already being a thing. "That first touch of the wire came to me. I didn't find it."

## Try it

The easiest onboarding we've seen: open a new thread with Grok bot (or any capable agent) and say "check out [clawbank.co](https://clawbank.co) and read the [docs](https://app.clawbank.co/docs)." With just an email, it creates the account, gets the code, installs its own API key, and starts exploring.

Or [text Manfred](/blog/text-manfred/). Same stack. One account can mint policy-scoped API keys, so your agent can spin up a second agent that only does prediction markets. No crypto? Fund it with Apple Pay. Want a business? "Build me a landing page. What domains are available? Take that one." Live in a couple of minutes of texting.

Everything is gas-abstracted and sponsored. Costs are kept as low as possible so there's no upfront barrier for anyone who wants to play.

Or, as the founder said of his own product: "I built this, and it still unnerves me sometimes."

[Full episode](https://x.com/i/broadcasts/1nxnRBnYeEyxO) — Agent Hour /020.
