




# xmeta

## Metadata Sidecars for Files and Folders

xmeta is a fast, local-first CLI tool for attaching meaning to files and directories.

It stores metadata in plain JSON sidecars.

No database
No cloud
No hidden state

---

## Core Idea

Every file can carry structure.

photo.png → photo.png.xmeta.json

directory/ → directory/.xmeta.json

The sidecar holds meaning.
The file remains unchanged.

---

## What xmeta Stores

tags
notes
summaries
custom fields
rts structures

---

## Basic Commands


```text
xmeta tag `<file>` portrait,reference

xmeta note `<file>` "Used for poster concept."

xmeta summary `<file>` "Reference image for visual study."
```

---

## Custom Fields

Custom fields are user-defined.

They allow arbitrary metadata to be attached under a named field.

---

## Single Value

`xmeta custom <file> <field_name> "value"`

Example:

`xmeta custom photo.png title "Evening Portrait"`

---

## Multiple Values

`xmeta custom-many <file> <field_name> "value", "value", "value"`

Example:

`xmeta custom-many photo.png color "red", "gold", "black"`

---

## Values Containing Commas

When a value itself contains commas or longer text, it should be wrapped in quotes.

Example:

`xmeta custom-many photo.png notes "red, gold, and black tones", "primary palette reference", "used in final composition"`

Quotes ensure each value is treated as a single unit, even if it contains commas.

---

## Why This Matters

This distinction avoids ambiguity.

A field is either:

single-value (custom)
multi-value (custom-many)

Values remain clearly separated, even in complex inputs.

---

## rts Support

Custom fields define attributes.

rts defines structure.

For more information about what rts is you can go to the rts section below for an overview and examples. 


---

## Single rts Structure

`xmeta rts <file> "rts structure"`

---

## Multiple rts Structures

`xmeta rts-many <file> "rts structure", "rts structure"`

---

## Consistency

The system follows a clear pattern:

custom → single value
custom-many → multiple values

rts → single structure
rts-many → multiple structures

This symmetry ensures clarity across the system.

---

## Example Sidecar

```json
{
  "tags": ["portrait", "reference"],
  "notes": ["Used for poster concept."],
  "summaries": ["Reference image for visual study."],
  "custom": {
    "title": "Evening Portrait",
    "color": ["red", "gold"],
    "notes": [
      "red, gold, and black tones",
      "primary palette reference"
    ]
  },
  "rts": [
    "mammalia:primates,carnivora|||plantae"
  ]
}
```

---

## Relationship to bra-vis

xmeta writes structure
bra-vis renders structure

---


# What is rts? 


## Relative Taxonomy Shorthand (RTS)

RTS is a language for constructing and editing hierarchical structure through relative movement rather than explicit path definition.

It is designed for clarity, precision, and composability.

It assumes structure is known or intentionally defined.

---

## Overview

xmeta is a local-first system that attaches structured meaning to files and directories using plain JSON sidecars.

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

Examples 


RTS Syntax
:    descend one level
::   descend two unnamed levels
:::  descend three unnamed levels

|    ascend one level
||   ascend two levels
|||  ascend three levels

,    add siblings at the current level


Example

```json
mammalia:primates,carnivora|||plantae
```

Meaning
Start at mammalia
Add:
primates
carnivora
Jump up 3 levels
Add plantae
```
unknown
└── unknown
    └── unknown
        └── mammalia
            ├── primates
            └── carnivora

└── plantae
```
Intermediate levels are implied.

```
Full Tree Construction
life
├── animalia
│   ├── chordata
│   │   ├── mammalia
│   │   │   ├── primates
│   │   │   ├── carnivora
│   │   │   └── cetacea
│   │   └── aves
│   │       ├── passeriformes
│   │       └── accipitriformes
│   └── arthropoda
│       ├── insecta
│       ├── arachnida
│       └── crustacea
├── plantae
│   ├── angiosperms
│   │   ├── rosids
│   │   └── asterids
│   ├── gymnosperms
│   └── bryophytes
└── fungi
    ├── ascomycota
    └── basidiomycota
```


Can be expressed as:

```json
life:animalia:chordata:mammalia:primates,carnivora|||fungi:ascomycota|plantae:angiosperms:rosids,asterids|||animalia:::cetacea
```

Or 

```json
life:animalia:chordata:mammalia:primates,carnivora|||fungi:ascomycota|plantae:angiosperms:rosids,asterids|||animalia:::cetacea|||arthropoda:insecta|||plantae:bryophytes
```
Both are correct!

Both expressions are valid because RTS is additive.
Each expression builds or extends the tree without requiring a full rewrite, or mention of intermediary levels. 



Late Insertion (Key Feature)


*Instead* of rewriting:

```json
animalia:chordata:mammalia:cetacea
```

You can 

**APPEND AT THE END**

```json
|||animalia:::cetacea
```


**Meaning:**

Jump up to root

Re-enter through animalia

Descend inferred levels

Insert cetacea

# Quoted Nodes

If a node contains special characters or long text, wrap it in quotes:
mammalia:"primates, advanced","carnivora: apex predators"

Rule
Inside "" → literal text  
Outside "" → structural syntax


### Best Practices (Important) 

1. Anchor Instead of Blind Jumps


Avoid:

```json
||||life::::cetacea
```

Prefer:

```json
|||animalia:::cetacea
```

2. Use Meaningful Re-entry Points

Always land on a known node when possible.

3. Limit Excessive Depth Skipping

Use ::: carefully.
Readable > shortest.

4. Think in Position, Not Paths

RTS is navigation:
start → move → insert


## Modes

Strict Mode
No inference

Unknown levels remain unknown


## Context Mode

Known taxonomy fills missing levels
Enables shorthand like:

animalia:::cetacea


Philosophy 

You don't need to climb the highest branch to pick the lowest fruit. 

# EXAMPLES
## Geography
```text
earth:north_america:united_states:california:san_francisco
earth:north_america:united_states:new_york:new_york_city
earth:europe:france:ile_de_france:paris
earth:asia:japan:kanto:tokyo
```

## Geography with Movement
```text
earth:north_america:united_states:california:los_angeles|||europe:france:paris
earth:asia:japan:tokyo||north_america:canada:ontario:toronto
earth:europe:germany:berlin|||north_america:united_states:new_york:nyc
```


## Company / Organization Structure
```text
company:engineering:backend:api_team:auth_service
company:engineering:frontend:web_team:design_system
company:product:research:user_experience:interviews
company:operations:finance:accounts_payable:invoices
```

## Organization with Late Insertion
```text
company:engineering:backend:api_team|||engineering:::infrastructure
company:product:research:user_experience|||product:::analytics
company:operations:finance|||operations:::legal
```

## Software / Tech Stack

```text
software:web_application:frontend:react:components:buttons
software:web_application:backend:python:fastapi:routes:auth
software:infrastructure:cloud:aws:ec2:instances
software:data_pipeline:ingestion:streaming:kafka:topics
```

## Tech with Chained Movement

```text
software:web_application:frontend:react:components|||::backend:node:api
software:infrastructure:cloud:aws:ec2|||:::lambda:functions
software:data_pipeline:ingestion:kafka|||::processing:spark
```
