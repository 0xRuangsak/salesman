Great question, and honestly one of my favorites, because it touches on something that trips up genuinely everyone at some point! So, if I'm understanding you correctly, and please do stop me if I'm not, you have a React component, a component in the React library (React), and it is re-rendering, which is to say rendering again, more often than you would like it to, and you would like to understand why.

Before I get to the answer, a little background. React decides whether to re-render a component by comparing the props it received last time with the props it receives this time, and that comparison is a shallow comparison, meaning it checks whether each prop is the same reference, not whether it has the same contents. This is, I should say, not a bug, never a bug, and under no circumstances a bug; it is simply, really, basically how React works.

Which brings us to the answer. In all likelihood, though I'd want to see the code to be completely certain, and I'm fairly certain, you are creating a new object reference on every render, most likely by passing an inline object literal as a prop, and because that object is a new reference each time, React's shallow comparison, the comparison I mentioned above, sees a different object every single time and re-renders.

To recap: new object each render, shallow comparison sees a change, component re-renders. Three things, and they happen in that order.

But wait, there's more. The fix, which is to say the remedy, is to memoize the object with the `useMemo` hook, so that the same reference, the very same object, is handed to the component on every render until its dependencies change. Here is what that looks like in full:

```jsx
import { useMemo } from "react";

function Parent({ userId }) {
  const options = useMemo(() => ({ userId, verbose: true }), [userId]);
  return <Child options={options} />;
}
```

Walking through it line by line: line 1 imports `useMemo` from React, the hook we will use; line 3 declares the parent component; line 4 calls `useMemo` with a function that builds the options object and a dependency array containing `userId`, so the object is rebuilt only, and I mean only, when `userId` changes; line 5 passes that stable object down to `Child`. In other words, the object is created once per distinct `userId` instead of once per render.

Pro tip: if you find yourself memoizing a lot of props, that is often, not always, but often, a sign that the child could be wrapped in `React.memo` as well.

Act now, because every render you don't need is a render you're paying for. I'd be happy to look at the actual component with you, I'd be glad to help you add a render-count test so this never regresses, and I'd love to walk through the rest of your props to see whether any others are being recreated each render.

P.S. Great question, truly.

P.P.S. Don't wait on this one.
