# Scaling Scrum the Scrum Way

https://justiceconder.medium.com/scaling-scrum-the-scrum-way-95f48884b43f

2020-05-19

![Image 4](https://miro.medium.com/v2/resize:fit:640/1*3e6IEMx5B-njrvHzYXe0dw.jpeg)

There are entire ecosystems of process frameworks that claim to scale agile. Most of them bring in a host of new roles, activities, and abstractions. This can be and should be a real concern for an organization already doing well. This is precisely the rub. If you find yourself in a position to significantly grow, it probably means you are doing things well. And if you are are doing well, what you’re doing is already working. So why would you upend everything and adopt a totally foreign process? That’s scary. It should be scary.

Growth does not come without risk. And the risk is not simply not improving relative to the investment received. The risk is that your organization actually slows down and becomes far less effective than you were prior to trying to scale. This actual risk is worse than the principle of diminishing returns, which states that additions to an input yield progressively smaller, or diminishing, increases in output. No, this new risk is captured in Brooks Law. The first formulation of Brooks Law states that adding resources to a late software project makes it slower.

There has been no small amount of research done in this area and the principal causes of the slowdown described in Brooks Law are as follows:

1.   Indivisible work. Nine women can’t make a baby in one month.
2.   Onboarding time. Adding resources saps the time of existing productive resources.
3.   Communication channel overhead. Everyone working on the same task needs to keep in sync, so as more people are added they spend more time trying to find out what everyone else is doing. Consider three feature teams that need to maintain general alignment on technical architecture and product vision. There are three possible lines of communication between them. One line between each team. Now let’s double that to six teams. There are now 15 lines of communication between those teams. A 100% increase in resources has created a 400% in coordination overhead. Let’s assume you are fortunate enough to need to grow your team resources by 200%. This takes your coordination overhead to 1100%! As you can see, this is untenable and we are only talking about the implications of moving from 3 to 9 teams.

Without blindly adopting any one of the highly complex scaled agile systems, what can be done to keep your organization’s existing cadence and address the above problems? Before we address each of these points, there is good news. If you are reading this in anticipation of growth and a scaling challenge, you have already won a significant battle. The most important thing an organization can do to prevent Brooks Law is to get in front of it and address it before it happens. Fixing the scaling problem before it happens is the most effective measure for preventing it. If this is not the case and you are already feeling the pain of growing inefficiencies, there is hope. We’re going to step through each cause and address them with proven mitigation strategies.

 

To address the divisibility problem, ensure you are organized around user-facing features leveraging feature teams. This might seem obvious because if you are already “doing Scrum” then you are already organized in this way. But, sadly, it is very possible to use the language of scrum while not practicing scrum at all. Let’s review a few things that should be true if you are really operating in a feature team way. To review, a feature team is “a cross-functional and cross-component team that can pull end-customer features from the product backlog and complete them.” This setup has a number of practical consequences.

*   A feature team should have dedicated, not frequently changed, team members.
*   Feature teams should deliver new “vertically sliced” capabilities (stories) and not just a stream of indiscriminate engineering tasks.
*   A feature team should work within a clearly defined feature area with a bounded context.
*   Feature teams should employ micro-services and micro-frontends in order to retain autonomy and maintain decoupling from one another.

The above practices address the divisibility problem by slicing an application up by feature areas and works backward from the highest point of value, user-facing capabilities.

To mitigate the ramp-up problem, implement the following strategies:

*   Build new teams by seeding them with existing experienced people.
*   Make the engineering onboarding runway-to-productivity as short as possible. Get a baseline for how long it takes new engineers to be productive and then try to cut that time my introducing things like turn-key environment setups and automatically generated useful documentation.
*   Capture and reuse learning sessions in the form of instructional videos that can be consumed later by new folks during the onboarding process.

To reduce communication-channel overhead, implement the following measures:

*   A recurring scrum-of-scrums to address feature team coordination.
*   Architecture meetings for each tribe to socialize design patterns.
*   Iterative delivery practiced in such a way that new features get merged every sprint to ensure convergence, not divergence.

To be perfectly clear, I’m not arguing that there’s no place for scaling frameworks, I’m merely suggesting that there are options for addressing scaling needs without immediately jumping to an entirely different process framework than the one your organization is already practicing. You will notice that no new concepts or abstractions were added to vanilla scrum in any of the above suggestions. It may be that you introduce a few of these practices over time like a good empirical process control person should and then see how things go. It is a natural tendency for organizations to crumble under their own complexity so we seek to minimize that through simplicity. The idea is to be iterative in these changes and not sudden and yet, at the same time, in front of potential problems. In future posts, we’ll discuss some practical applications of the above in the form of what a sprint calendar could look like and how to use the concept of a tribe to socialize good and consistent design patterns across a multitude of feature teams.
