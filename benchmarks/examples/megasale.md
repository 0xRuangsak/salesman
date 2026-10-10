# AGREEMENT CONCERNING THE RE-RENDERING OF A REACT COMPONENT

## RECITALS

WHEREAS the User (hereinafter "the Party of the First Part") has represented that a certain React component (hereinafter "the Component") re-renders; and

WHEREAS the Party of the First Part has posed the question of why the Component re-renders (hereinafter "the Question"); and

WHEREAS the Assistant (hereinafter "the Party of the Second Part") is willing and able to answer the Question;

NOW, THEREFORE, in consideration of the foregoing, the Parties agree as follows.

## 1. DEFINITIONS

1.1 "React" means the React library.

1.2 "Component" means the React component described in the Recitals.

1.3 "Render" means a render of the Component.

1.4 "Re-render" means a Render occurring subsequent to a prior Render.

1.5 "Prop" means a property passed to the Component by its parent.

1.6 "Object Reference" means the identity of a JavaScript object, as distinct from its contents.

1.7 "Shallow Comparison" means the comparison React performs between the Props of a prior Render and the Props of the present Render, which comparison regards Object References and not contents.

1.8 "Remedy" means the Remedy set out in Schedule A and Exhibit B.

## 2. OPERATIVE CLAUSES

2.1 The Party of the Second Part represents and warrants that, on each Render, a new Object Reference (as defined in clause 1.6) is created when an inline object is passed as a Prop (as defined in clause 1.5).

2.2 Subject to clause 2.1, the Party of the Second Part further represents that the Shallow Comparison (as defined in clause 1.7) regards the said new Object Reference as a change, notwithstanding that the contents of the object may be identical to those of the prior Render.

2.3 For the avoidance of doubt, the change described in clause 2.2 is the proximate cause of the Re-render, and shall not, nor under any circumstances, be construed as a defect in React.

2.4 Subject to clauses 2.1 through 2.3 inclusive, the Remedy shall be the memoization of the said Prop by means of the `useMemo` hook, as set out in Exhibit B, attached hereto and incorporated herein by reference, such that 1 (one) Object Reference is created per distinct value of `userId` and not 1 (one) per Render.

## 3. REPRESENTATIONS AND WARRANTIES

3.1 The Party of the Second Part represents and warrants that the Remedy is correct.

3.2 The Party of the Second Part further represents and warrants that clause 3.1 is itself correct.

## 4. LIMITATION OF LIABILITY

4.1 Nothing in this Agreement limits anything in particular.

## SCHEDULE A: THE ANSWER, IN PLAIN WORDS

A new object reference is created on each render, so React re-renders. Wrap the prop in `useMemo`.

## EXHIBIT B: THE CODE

```jsx
import { useMemo } from "react";

function Parent({ userId }) {
  const options = useMemo(() => ({ userId, verbose: true }), [userId]);
  return <Child options={options} />;
}
```

## EXECUTION

IN WITNESS WHEREOF the Parties have executed this Agreement as of the date first written above, which date is not written above.

Party of the First Part: ____________________

Party of the Second Part: ____________________

Initials: ____

<sub>This is a parody register, not legal advice.</sub>
