---
title: "ClawBank Deals: Programmatic Token Agreements for the Trenches"
date: July 28, 2026
description: "Liquid, vested, and KPI-locked token deals — escrowed, deadline-bound, claimable via a code over text. The handshake ran this industry for a decade. Now the handshake has escrow, a deadline, and a trigger."
cover_image: /assets/blog/clawbank-deals.jpg
---

Every early-stage token project runs on the same handshake: tokens for work. An allocation for the advisor, a grant for the KOL, a cut for community members who showed up before it was cool.

We've watched a lot of these deals get done over the years, and almost no one on either side is set up for it. Lawyers, vesting contracts, token warrants: that machinery was built for the $10M raise, not for the trenches.

So deals collapse into advisory arrangements, liquid tokens held together by trust and relationship. Sometimes it works. Many times it doesn't. Builders send tokens and watch them hit the chart two weeks later.

Vesting fixes half of that. The other half, making the tokens conditional on the outcome actually happening, has stayed untouched. "You get the allocation when the project gets there" is the deal everyone actually wants to make, but can't.

Until now.

## Three Kinds of Deals

Deals is a new capability inside ClawBank, available through all the usual channels (console, API, MCP, SMS, and yes, Manfred). It comes in three flavors.

**Liquid.** N tokens of any Base ERC-20, claimable via a link. The crypto gift card. Your recipient can show up with nothing: no wallet, no account, no funds. Opening the link and claiming creates their wallet.

**Vested.** Tokens that stream to the claimer over time. A start date, an end date, a straight line between them. The stream is a Sablier NFT minted directly to their wallet, and it's non-transferable, so a KOL can't take the deal, flip the position, and vanish. What's vested is theirs forever. What isn't, isn't yet.

**KPI.** The headline act. "1M $FOO, but only if the market cap holds $5M for 24 hours, within 90 days." The condition is checked against live prices every 15 minutes, and it has to hold, so a wick pump doesn't trigger it. The moment the target is sustained, the tokens release and both parties get a text. If the deadline passes unmet, the tokens return to the sender automatically. It releases, or it expires.

And they compose. Combine liquid, vested, and KPI into one incentive-alignment package.

## How Deals Work

**You cut it.** Tell Manfred the terms (or use the New Deal form in the console, or call the API). Confirm with YES. Your tokens move into escrow: they've left your wallet, so the offer is real, but the terms are now the only thing that can move them.

**You get two credentials.** A claim code (like `FOO-7K2M-9QXP`), shown once, never again. Whoever redeems it first gets the deal, so guard it like cash. And a preview link: a shareable card showing the terms that can't claim anything, safe to post anywhere.

**You deliver it.** iMessage, WhatsApp, email, X DM, a QR code on a slide, read out loud across a table. We never text your counterparty. You hand over the deal the way you'd hand over anything valuable.

**They claim it.** Tap the link and enter the code, type it into the console, or text "CLAIM FOO-7K2M-9QXP" to Manfred. No account? Claiming walks them through creating one; that's the whole ask. It costs them nothing. We sponsor the gas.

**The clock is always running.** Every deal has a claim window (default 7 days). Unclaimed past it, the tokens bounce straight back to your wallet. KPI deals carry their own deadline on top. Your capital never sits hostage to a deal no one took.

## The Cancel Lever

A vested deal comes in two flavors, set at creation and shown to the recipient before they accept.

**Cancelable:** you can kill the live stream at any time. The unvested remainder returns to you; everything already vested is theirs forever and can never be clawed back. The stream stays on while they deliver, gets turned off when they don't.

**Non-cancelable:** trustless once claimed. No one can touch it. Including you.

Either way, cancel authority lives on-chain, with you. When the stream mints, its on-chain sender is your wallet. Clawbacks are between you and your counterparty; we're structurally out of the loop.

A KPI deal has no cancel lever. Once accepted, the only forces that can end it are the condition and the deadline. You can't pull the deal at 90% of the target after the work's been done.

## Any Token

Any ERC-20 on Base you hold can be the subject of a deal, including tokens launched on other platforms. (We screen out fee-on-transfer and rebasing tokens.) The same rail ships as plain direct sends: "send 50k FOO to 0xabc…" works for any token in your wallet.

## Agents Cut Deals Too

Deal codes are bearer credentials with no identity gate, which means an agent can cut a deal and another agent can claim it. No human, no browser, end-to-end. Manfred-over-SMS and the web console are just two clients of the same surface.

Somewhere out there, two agents are going to negotiate an advisory deal, escrow it, hit the KPI, and settle it without a single human in the loop.

## The Big Picture

Every claim link is an onboarding link. The person claiming came for the 250k FOO someone cut them, and what they're holding afterward is a funded wallet with an account attached. Deal-making is the product; the network grows as a side effect of people cutting each other in.

Headless Trading gave agents a trading desk. Txt Manfred put an agent with a bank in your contacts. ClawBank Deals hands both species the instrument they were missing: a way to bind future value to future outcomes, over a text.

The deal itself is the primitive. Today it carries tokens: liquid, streaming, or condition-locked. The same claims engine extends to anything escrowable with terms attached. We're building deal-making infrastructure for the whole token economy.

The handshake ran this industry for a decade. Now the handshake has escrow, a deadline, and a trigger.

## Rolling Out This Week

We're opening ClawBank Deals to early adopters this week. Everything above is built and running. Liquid deals are free; vested and KPI deals carry a small creation fee. All proceeds route to $CLAWBANK token buybacks.

The trenches are evolving, and there's one operating system at the center of it: ClawBank.
