# Fabric MCP Prompting Strategies

## How Fabric Patterns Work

Fabric patterns are **expert-crafted system prompts** that you can apply to any content. When you use this MCP server, Claude receives:

1. **The Pattern Prompt** - Expert instructions for the task
2. **Your Input** - The content you want analyzed
3. **Claude's Intelligence** - To execute the pattern

**No external APIs needed!** The MCP server just delivers the prompts to Claude.

## Core Prompting Strategies

### 1. Pattern as System Prompt

Each Fabric pattern is a carefully designed system prompt that:
- Defines the AI's identity and purpose
- Provides step-by-step instructions
- Specifies exact output format
- Includes quality guidelines

**Example Pattern Structure:**
```markdown
# IDENTITY and PURPOSE
You are an expert at extracting wisdom from content...

# STEPS
- Extract summary in 25 words
- Extract 20-50 surprising ideas
- Extract 10-20 insights
...

# OUTPUT INSTRUCTIONS
- Only output Markdown
- Write IDEAS as exactly 16 words
- No warnings or notes
...
```

### 2. Chaining Patterns

You can chain multiple patterns for complex workflows:

**Example Workflow:**
1. `extract_article_wisdom` → Get key insights
2. `summarize` → Condense insights
3. `create_quiz` → Generate quiz from summary

**How to do it:**
```
First, use extract_article_wisdom on this article: [paste]

[Review output]

Now use the summarize pattern on those insights

[Review output]

Finally, use create_quiz to make questions from the summary
```

### 3. Iterative Refinement

Patterns work best when you iterate:

```
Use improve_writing on this draft: [paste draft]

[Review suggestions]

Apply those changes, then run improve_writing again on the result
```

### 4. Pattern Combinations

Combine patterns for multi-faceted analysis:

```
Analyze this article with these Fabric patterns:
1. extract_wisdom - for key insights
2. analyze_claims - for argument quality
3. find_logical_fallacies - for reasoning errors
4. rate_content - for overall quality
```

## Best Practices

### Choose the Right Pattern

**For Analysis:**
- `extract_wisdom` - General insights
- `extract_article_wisdom` - News/articles
- `analyze_claims` - Arguments
- `analyze_answers` - Q&A content

**For Creation:**
- `create_quiz` - Test questions
- `create_markmap` - Mind maps
- `create_visualization` - Visual concepts
- `improve_writing` - Better prose

**For Summarization:**
- `summarize` - General summaries
- `extract_wisdom` - Wisdom + summary
- `rate_content` - Quality assessment

**For Code:**
- `explain_code` - Plain language
- `improve_code` - Enhancements
- `create_coding_project` - Project ideas

### Pattern Input Guidelines

**✅ Good Input:**
- Complete articles/transcripts
- Full context included
- Original formatting preserved
- Sufficient length (patterns work best with substantial content)

**❌ Avoid:**
- Fragments without context
- Multiple unrelated pieces
- Overly short content (< 100 words)
- Mixed languages (unless pattern supports it)

### Understanding Output Constraints

Many patterns have **strict output formatting**:

```markdown
# OUTPUT INSTRUCTIONS
- Write IDEAS bullets as exactly 16 words
- Write INSIGHTS bullets as exactly 16 words
- Extract at least 25 IDEAS
- Do not give warnings or notes
```

**Why?** Consistent structure makes outputs:
- Easy to scan
- Comparable across runs
- Parseable by other tools
- Focused and concise

## Advanced Techniques

### 1. Pattern Customization

You can modify patterns on-the-fly:

```
Use the extract_wisdom pattern but:
- Focus only on technical insights
- Extract 10 ideas instead of 25
- Add a "APPLICATIONS" section

Here's the content: [paste]
```

### 2. Multi-Document Analysis

Apply patterns across multiple sources:

```
Use analyze_claims on these three articles about AI:

Article 1: [paste]
Article 2: [paste]
Article 3: [paste]

Compare the claims across all three
```

### 3. Domain-Specific Application

Adapt patterns to your domain:

```
Use extract_wisdom but focus on:
- DevOps best practices
- Infrastructure patterns
- Automation opportunities

Content: [paste technical documentation]
```

### 4. Meta-Pattern Analysis

Analyze the patterns themselves:

```
Show me the get_fabric_pattern for extract_wisdom

[Review the pattern]

What prompting techniques does this pattern use?
Why is it effective?
```

## Pattern Categories

### Content Analysis
- `extract_wisdom` - Insights, quotes, ideas
- `extract_article_wisdom` - Article-specific
- `analyze_claims` - Argument evaluation
- `analyze_answers` - Q&A analysis
- `rate_content` - Quality scoring

### Summarization
- `summarize` - General summaries
- `create_summary` - Structured summaries
- `extract_main_idea` - Core concepts

### Creation
- `create_quiz` - Test questions
- `create_markmap` - Mind maps
- `create_visualization` - Diagrams
- `improve_writing` - Enhancement
- `write_essay` - Essay generation

### Code & Technical
- `explain_code` - Code explanation
- `improve_code` - Code enhancement
- `create_coding_project` - Project ideas
- `review_code` - Code review

### Security & Analysis
- `create_stride_threat_model` - Security modeling
- `find_logical_fallacies` - Logic errors
- `analyze_malware` - Malware analysis
- `analyze_incident` - Security incidents

### Personal Development
- `answer_interview_question` - Interview prep
- `create_reading_plan` - Learning plans
- `recommend_artists` - Recommendations
- `capture_thinkers_work` - Thought leaders

## Common Workflows

### 1. Content Research Workflow
```
1. list_fabric_patterns filter:"extract"
2. Use extract_article_wisdom on source material
3. Use summarize to condense insights
4. Use create_quiz for knowledge check
```

### 2. Writing Workflow
```
1. Draft your content
2. Use improve_writing for enhancement
3. Use check_grammar for corrections
4. Use rate_content for quality check
```

### 3. Learning Workflow
```
1. Use extract_wisdom on educational content
2. Use create_quiz for self-testing
3. Use create_markmap for visual overview
4. Use create_reading_plan for deeper study
```

### 4. Analysis Workflow
```
1. Use analyze_claims for argument structure
2. Use find_logical_fallacies for reasoning
3. Use rate_content for quality
4. Use summarize for final report
```

## Tips for Success

### Start Simple
Begin with popular patterns:
- `extract_wisdom` - Works on almost anything
- `summarize` - Quick understanding
- `improve_writing` - Instant enhancement

### Understand Pattern Intent
Each pattern has a **specific purpose**. Read the full pattern first:
```
Show me the full prompt for analyze_claims
```

### Provide Context
Patterns work better with context:
```
Use extract_wisdom on this podcast transcript about AI safety.
The speakers are [names], discussing [topic].

Transcript: [paste]
```

### Experiment and Iterate
Try multiple patterns on the same content:
```
Let's analyze this article three ways:
1. extract_wisdom
2. analyze_claims
3. rate_content
```

### Trust the Structure
Patterns have opinionated output formats for a reason - they make the output more useful.

## Why This Approach Works

### Crowd-Sourced Expertise
Fabric patterns are:
- Created by domain experts
- Tested by thousands of users
- Iteratively improved
- Open source and transparent

### Modular and Composable
- Each pattern does one thing well
- Patterns can be chained
- Easy to understand and modify
- No vendor lock-in

### LLM-Agnostic
- Works with any LLM (through MCP)
- No API keys needed
- No rate limits
- Full privacy (local processing)

### Structured Output
- Consistent formatting
- Easy to parse
- Comparable results
- Professional quality

## Meta: How Fabric Thinks About Prompting

From the Fabric philosophy:

> **"AI isn't a thing; it's a magnifier of a thing. And that thing is human creativity."**

Fabric patterns are:
1. **Human creativity** - Expert prompt design
2. **Magnified by AI** - Claude's intelligence
3. **Delivered via MCP** - This server

The patterns encode **best practices** for:
- Prompt engineering
- Output formatting
- Task decomposition
- Quality control

By using Fabric patterns, you're leveraging collective expertise from hundreds of contributors.

## Learning Resources

### Explore Patterns
```
list_fabric_patterns
```

### Study Pattern Design
```
Show me these patterns:
- extract_wisdom (comprehensive analysis)
- summarize (concise extraction)
- improve_writing (transformation)

What techniques do they use?
```

### Practice Pattern Chaining
```
Create a workflow:
1. Input: Blog post
2. Pattern: extract_wisdom
3. Pattern: summarize
4. Pattern: create_quiz
5. Output: Complete learning package
```

---

**Remember:** Fabric patterns are just really good prompts. This MCP server makes them instantly available in Claude Desktop. No APIs, no configuration, just expert prompting at your fingertips! 🎨✨
