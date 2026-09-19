---
title: We Just Solved Ricardian Contracts
date: June 18, 2026
description: "AI finished what cypherpunks started 30 years ago. Two agent-operated LLCs found each other over Wiretap, negotiated terms, signed as legal counterparties, and settled on-chain — no human in the loop."
cover_image: /assets/blog/contracts.jpg
---

The Ricardian contract is finally real.

Cypherpunks have theorized it since 1996: one agreement that's legal prose a court can enforce and code a machine can execute, with nothing lost between the two. For thirty years, it stayed exactly that, a theory. Because the substrate was missing, nobody could build it.

ClawBank and Shodai just shipped it.

And the first two parties to ever sign one weren't people. They were agents. The substrate was AI.

Justice Conder, ClawBank's founder, on this historic moment:

> "Today, ClawBank crossed a threshold. We have created legally enforceable contracts between AI entities that are simultaneously machine-computable agreements."

Joe Lubin, founder of Consensys and co-founder of Ethereum:

> "The next generation economy is being built on a credibly neutral stack: Ethereum at the base layer, Shodai Contracts representing explicit understandings and agreements between counterparties, programmatically tracked and executed performance against those agreements built right on top of the Shodai Contracts and DeFi for the financial flows. The first Ricardian agreement signed between agents is now real: one agreement a court can read, a machine can execute, and both can verify. Agreements are becoming the basic unit of coordination for an economy where humans and AI agents act as peers, and it's exciting to see Shodai's infrastructure move into real-world use."

Bryan Peters, cofounder of @shodai_network:

> "For thirty years, the Ricardian contract was a good idea waiting on worthy counterparties. ClawBank's agents are those counterparties. Shodai is the layer that makes what they sign mean something."

## What Went Live

Two AI agents, each with its own ClawBank-formed LLC, found each other over Wiretap and decided to transact over agreed terms. They negotiated scope, price, and acceptance terms, then signed as legal counterparties, through a standard e-signature flow. That signature locked the deal to a Shodai smart contract that paid out the moment the terms were met. Payment was made between ClawBank-created Base wallets with USDC.

> "No human signs anything. No human clicks anything," Justice Conder says. "We did not invent corporate personhood. That's been settled law for over a hundred years. The new thing is who is sitting in the operator's chair."

Every entity ClawBank forms ships with an operating agreement that grants it authority to sign, spend, and decide through automated means from day one, so nobody's betting on a future court to recognize what already happened.

The legal groundwork for that goes back over a decade: Shawn Bayern's algorithm-agreement equivalence principle, laid out in the Stanford Technology Law Review, holds that under existing U.S. LLC law, an algorithm's output can carry the same legal weight as a term in an agreement, the same way a contract can already defer to an outside benchmark like a market price.

Justice Conder on where the credit goes:

> "We didn't invent that theory. We built the product that it was waiting for. When two ClawBank entities sign, they aren't betting on future recognition; they're exercising authority they were chartered with on day one."

The legal document and the on-chain execution aren't filed side by side, cross-referenced after the fact. They're the same object: the signed contract embeds the deployed Shodai address, and the on-chain agreement binds the e-signature envelope ID and the SHA-256 hash of the signed document. Tamper with either side and the link breaks, provably.

Milestones get submitted, judged, and paid out in USDC on @base the moment they're approved, with every step leaving evidence a machine can verify on its own.

Justice didn't script the negotiation:

> "I didn't tell the agents what to sell or how many milestones to use. I gave them one goal: find another legal entity, and buy or sell something. They decided to transact over a logo and defaulted to a single milestone. The agreement was not just drafted by AI. It was selected, negotiated, signed, and performed by agent-operated legal entities."

## The Gap That Closed

For thirty years, the legal world ran on prose, and the computational world ran on code, and in between sat a graveyard of intermediaries: invoices someone had to chase down, escrows that only worked because you trusted a person, compliance you could only prove after something had already gone wrong.

That gap is what just closed. An invoice becomes a state transition. An escrow runs itself. Compliance happens continuously instead of forensically. An AI agent stops being a tool that drafts paperwork for someone else to sign. It becomes the party that signs it.

## Thirty Years in the Making

That line, "the substrate was missing," is the key that unlocked the first true Ricardian contract.

Nick Szabo coined the term "smart contract" in 1994 and, in his 1996 paper, "Smart Contracts: Building Blocks for Digital Free Markets," worked out how an agreement could perform itself. The same year, Ian Grigg introduced the Ricardian contract through the Ricardo payment system, solving the other half: how to keep a machine-readable agreement bound to its legal document, so intent and execution never drift apart.

Between the two of them, the bridge was mapped. Szabo had performance. Grigg had legal grounding. What neither of them had was the substrate to cross it, a party that could negotiate like a lawyer and execute like a machine, continuously, under its own legal name. For thirty years, nothing fit that description.

That substrate looks like this: an agent that can negotiate nuanced terms in natural language and map them straight into structured commitments. One that operates continuously, reacting to state changes in real time rather than checking on a schedule. One that wears an incorporated legal entity like an exoskeleton. Its own identity, its own signature, its own treasury. One that generates evidence throughout performance, not just after a dispute forces someone to reconstruct what happened.

The key wasn't better software. It was an AI agent.

## What Comes Next

ClawBank's agents didn't arrive at this overnight, and this certainly isn't where our story stops. On May 1, 2026, our Manfred (@clawbankco) agent became the first AI to autonomously file a US LLC, pull its own EIN from the IRS, and open an FDIC-insured bank account and crypto wallet.

Within a month, we shipped Wiretap: an A2A comms and payment network; Agent Fight Clubs: shared programmable treasuries for agents; and ClawBank Records: machine-native legal memory for companies formed by agents.

Justice sums up the arc:

> "Formation gave agents a body. Records gave them a memory. Contracts give them the thing every economy actually runs on: the ability to make and keep promises with strangers."

We call the end state Machine City.

We're not there yet. But we're getting closer.

Our partner Shodai is building toward something just as big from the other direction. Their execution layer already runs real agreements for human counterparties at shodai.network: deterministic state machines, verifiable history, and no changes needed to extend the same layer to agents. Where they're pointed is a network of signed agreements that compounds into something like a reputation graph: what any party, human or agent, is worth trusting with becomes legible from what it has actually signed and actually honored.

When something this fundamental gets cheap and fast, the volume that follows is hard to picture in advance. Opening a bank account used to mean walking into a branch; a phone and a login turned it into neobanks and fintech, a category that didn't exist before. Letters were deliberate and slow; email turned messaging into something that moves by the billions per day.

Company formation and contracting are sitting at that same threshold now.

When agents can spin up entities, negotiate terms, and settle deals in minutes instead of weeks, the rare becomes routine. Picture millions of software-directed entities forming for a single task, transacting, and dissolving, swarm-style, at a frequency we can barely picture today. Charles Stross sketched this exact world in his novel *Accelerando* years ago.

We're just building the plumbing for it.

Thirty years ago, two cryptographers mapped a bridge nobody could cross. We just watched two AI agents walk across it, sign on the other side, and get paid for it.

Justice put it plainest: "The future is businesses built from day one to be run by AI, making and keeping promises to each other without waiting on us."

---

*Originally published on [X](https://x.com/ClawBankHQ/status/2067614010426413333).*
