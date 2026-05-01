# xmeta

## Relative Taxonomy Shorthand (RTS)

RTS is a language for constructing and editing hierarchical structure through relative movement rather than explicit path definition.

It is designed for clarity, precision, and composability.

It assumes structure is known or intentionally defined.

---

## Overview

xmeta is a local-first system that attaches structured meaning to files and directories using plain JSON sidecars. :contentReference[oaicite:0]{index=0}

RTS is its core language.

It enables users to build, extend, and navigate hierarchical structures without rewriting full paths.

---

## The Problem

Traditional hierarchical systems require:

complete paths  
precise insertion points  
global awareness of structure  

As systems grow, these requirements become burdensome and error-prone.

---

## The RTS Approach

RTS replaces path definition with positional movement.

start anywhere  
move  
insert  

Structure is not rewritten.  
It is navigated.

---

## Core Capabilities

RTS allows:

precise placement without full path rewriting  
incremental extension of existing structure  
late insertion without structural disruption  
clear expression of hierarchy through movement  

---

## Structural Discipline

RTS is designed to be explicit where it matters.

Best practice favors:

anchored re-entry points  
clear structural intent  
minimal ambiguity  

While RTS permits shorthand, it is not intended to rely on ambiguity for correctness.

---

## Additive Behavior

RTS is additive.

Each expression contributes to structure without requiring modification of existing definitions.

Multiple valid expressions can describe the same structure from different positions.

---

## Chained Movement

RTS supports chained movement such as:

|||::

This represents:

ascend three levels  
then descend two levels  

In strict RTS usage, such expressions should ideally include meaningful anchors when possible:

|||mammalia::

This improves clarity and reduces ambiguity.

---

## Gaps and Representation

RTS itself does not resolve missing structure.

It expresses movement and intent.

When intermediate levels are not specified, they remain undefined at the language level.

---

## bra-vis

bra-vis is the interpreter for RTS.

It is responsible for rendering incomplete or partially specified expressions into visible structure.

Where RTS leaves gaps, bra-vis represents them explicitly.

It does this by:

using known indexed structure when unambiguous  
using local context when safe  
inserting unknown placeholders when necessary  

This ensures that even incomplete expressions remain legible and structurally honest.

---

## Index and Interpretation

bra-vis maintains an index of known nodes during interpretation.

This allows:

reuse of established structure  
resolution of chained movement when possible  
avoidance of unsafe assumptions  

When no safe resolution exists, unknown is used.

---

## What RTS Excels At

RTS is most effective when:

structure is large or evolving  
paths are costly to rewrite  
data is added incrementally  
multiple contributors extend a shared hierarchy  
relationships are known locally but not globally  

---

## Use Cases

filesystem annotation  
research classification  
taxonomy construction  
incremental knowledge systems  
exploratory hierarchical modeling  

RTS is particularly useful where:

structure grows over time  
completeness is not guaranteed at entry  

---

## Modes

Strict Mode  
no inference  
structure must be explicitly defined  

Context Mode (via bra-vis)  
structure may be resolved using known information when safe  

---

## Philosophy

RTS is built on:

local-first operation  
plain text representation  
composability  
inspectability  

It prioritizes:

clarity over compression  
correctness over convenience  

---

## Summary

RTS defines how structure is written.

bra-vis defines how structure is rendered.

Together, they allow:

precise expression  
flexible construction  
honest representation of incomplete knowledge  

---

## Final Principle

You do not need the full tree  
to place the correct branch
