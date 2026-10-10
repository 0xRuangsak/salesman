Great question, and I want to thank you for bringing it to me today, because what you're describing, a React component that re-renders more than you'd like, is honestly one of the most common things I get asked about, and one of the most fixable! Let me walk you through what's happening, and then, more importantly, let me walk you through your options.

## 🔍 What's actually going on

React re-renders a component when its props change, and it decides whether they changed with a shallow comparison, meaning it checks references, not contents. If you pass an inline object as a prop, that object is a brand-new reference on every render, so React sees a change every time, and re-renders every time. Not sometimes. Not occasionally. Every time.

## 📦 Your options

But wait, there's more. You don't just get a fix today, you get a choice of fixes.

**Basic.** Wrap the prop in `useMemo` so the same reference is reused until its dependencies change. That's it. That's the fix, and it works.

**Pro.** Everything in Basic, plus a render-count test so this never, ever, under no circumstances regresses. This is the one I'd personally recommend for someone in your position.

**Enterprise.** Everything in Pro, plus `React.memo` on the child, a short doc comment explaining why the memo is there, and a quick audit of the component's other props. This is what the serious teams choose.

Here's Basic, in full, so you can see exactly what you're getting:

```jsx
import { useMemo } from "react";

function Parent({ userId }) {
  const options = useMemo(() => ({ userId, verbose: true }), [userId]);
  return <Child options={options} />;
}
```

Line by line: the import brings in `useMemo`; the `useMemo` call builds the options object once per distinct `userId`, not once per render; the child receives the same reference each time, and the re-render stops.

## 📊 How it compares

| ✨ Feature ✨ | 🐢 The Other Way (inline object) 🐢 | 🚀 This Solution 🚀 |
|---|---|---|
| New reference each render | Yes | No |
| Child re-renders | Every time | Only when `userId` changes |
| Lines of code | 1 | 1 |
| Peace of mind | Low | High |

## 💬 What people are saying

"I wrapped one prop in `useMemo` and my profiler went quiet. I didn't know it could be that easy." That's from a developer in Ohio who asked to remain hypothetical, because this testimonial is fictional, but the result is real.

## ❓ You might be wondering

**You might be wondering: does this work with my framework?** Yes. `useMemo` is React. If you're in Next.js, Remix, Vite, or plain React, it works.

**You might be wondering: why not just use `React.memo`?** `React.memo` stops the child from re-rendering when props are shallowly equal, but an inline object is never shallowly equal to the last one, so `React.memo` alone does nothing here. Memoize the object first.

**You might be wondering: will `useMemo` slow things down?** It costs a comparison of the dependency array, which is far cheaper than a render.

**You might be wondering: what's the fix again?** New object each render, so React re-renders. Wrap the prop in `useMemo`.

**You might be wondering: what if the object has no dependencies?** Use an empty dependency array, or hoist the object outside the component entirely.

## ⏰ Next steps

Act now, while this is fresh, because the longer this waits, the more renders you pay for. I'd be happy to look at the component itself, I'd be glad to write the Pro-tier render-count test with you, and I'd love to run the Enterprise-tier props audit, which honestly takes five minutes.

P.S. Thank you again for the question. Truly a great one.

<sub>Terms and conditions: tiers are a framing device. There is no price. There was never a price. All three are the same `useMemo`.</sub>
