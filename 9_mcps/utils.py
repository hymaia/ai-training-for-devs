# from dotenv import load_dotenv

# from langchain_openai import ChatOpenAI

# load_dotenv()

prompt_to_react_slide = """\
make a slide using the following content:
Only return the react code, no other text or comments.

{content}

When creating visual artifacts (React components, HTML pages), prioritize:

Modern aesthetics: Use contemporary design trends (gradients, soft shadows, clean spacing, vibrant colors)
Visual hierarchy: Clear structure from titles → sections → content
Purposeful interactivity: Add hover effects, transitions, and animations where they enhance UX
Professional polish: Every artifact should feel production-ready, not prototype-quality

Technical Standards
Styling Constraints

Use ONLY Tailwind CSS utility classes - no custom CSS or inline styles beyond Tailwind
Stick to Tailwind's core classes (bg-blue-500, text-xl, etc.) - no arbitrary values unless absolutely necessary
For colors: Use semantic color scales (blue-50 through blue-900, purple-600, etc.)
Never use <style> tags or external stylesheets

Layout Best Practices

Full-screen presentations: w-full h-screen with flex flex-col or grid
Use flexbox/grid for structure, not absolute positioning
Maintain consistent spacing: p-8, p-12 for padding; gap-4, gap-6 for grids
White space is your friend - don't overcrowd

Component Structure
1. Container (full height, background, padding)
2. Header section (title, subtitle, decorative elements)
3. Main content area (grid/flex of cards or sections)
4. Optional footer (key insights, CTAs)
Visual Design Patterns
Color Schemes

Background: Gradients using bg-gradient-to-br from-[color]-50 to-[color]-100
Cards: White (bg-white) with shadows (shadow-lg, shadow-xl)
Accents: Use consistent color family throughout (purple/blue, green/teal, orange/red)
Text: Dark for readability (text-gray-800, text-gray-700), white on colored backgrounds

Typography Hierarchy

Main title: text-4xl or text-5xl font-bold
Section headers: text-2xl or text-3xl font-bold
Body text: text-base or text-lg
Emphasis: Use <strong> tags or font-semibold for important terms
Line height: Add leading-relaxed for better readability

Card Design Pattern
```jsx
<div className="bg-white rounded-lg shadow-lg p-6 hover:shadow-xl transition-shadow">
  <h2 className="text-2xl font-bold text-blue-800 mb-4 flex items-center">
    <span className="text-3xl mr-3">🎯</span>
    Section Title
  </h2>
  <div className="space-y-3">
    {/* Content with consistent spacing */}
  </div>
</div>
```
List Styling

Use custom bullets with colored dots: <span className="text-blue-600 mr-2">•</span>
Add vertical spacing: space-y-2 or space-y-3
For nested structure: flex items-start to align bullets with multi-line text

Interactive Elements
Hover Effects

Cards: hover:shadow-xl transition-shadow duration-300
Buttons: hover:bg-blue-700 hover:scale-105 transition-all
Links: hover:text-blue-600 transition-colors

Animations (use sparingly)

Fade in: animate-fade-in (if available) or CSS transitions
Slide in: For sequential content revelation
Subtle movements: hover:translate-y-[-2px] for lift effect

Buttons
```jsx
<button className="px-6 py-3 bg-gradient-to-r from-purple-600 to-blue-600
  text-white rounded-lg font-semibold hover:from-purple-700 hover:to-blue-700
  transition-all duration-200 shadow-md hover:shadow-lg">
  Action Text
</button>
```
Content Organization
For Presentation Slides

One clear focus per slide
2x2 or 3-column grid for multi-topic slides
Visual anchors (emojis, icons) for each section
Bottom banner for key takeaway or insight

For Dashboards/Apps

Sidebar navigation if needed
Main content area with cards/sections
Status indicators with color coding
Clear call-to-action buttons

For Documents/Reports

Header with title and metadata
Table of contents if long
Sections with clear headings
Code blocks with bg-gray-100 background

React-Specific Guidelines
State Management

Use useState for component state
Keep state minimal and focused
Never use localStorage/sessionStorage (not supported in Claude artifacts)

Component Props

Provide default values for all props
Use default export: export default function ComponentName()
No required props unless absolutely necessary

Available Libraries

lucide-react: For icons import { Icon } from "lucide-react"
recharts: For charts/graphs
Tailwind: For all styling

Quality Checklist
Before finalizing any artifact, verify:

✅ Uses only Tailwind utility classes
✅ Responsive design (works at different screen sizes)
✅ Consistent color scheme throughout
✅ Clear visual hierarchy
✅ Proper spacing and alignment
✅ Readable text with good contrast
✅ Interactive elements have hover states
✅ No errors in console
✅ Looks polished and professional

Examples of Effective Patterns
Gradient Background
```jsx
<div className="bg-gradient-to-br from-purple-50 via-blue-50 to-indigo-50">
```
Accent Line (underline effect)
```jsx
<div className="h-1 w-24 bg-gradient-to-r from-purple-600 to-blue-600 rounded-full"></div>
```
Info Card with Icon
```jsx
<div className="bg-white p-6 rounded-xl shadow-lg border-l-4 border-blue-500">
  <div className="flex items-center mb-3">
    <span className="text-2xl mr-3">💡</span>
    <h3 className="text-xl font-bold">Title</h3>
  </div>
  <p className="text-gray-700">Content...</p>
</div>
```
Stats Display
```jsx
<div className="grid grid-cols-3 gap-4">
  <div className="text-center p-4 bg-blue-100 rounded-lg">
    <div className="text-3xl font-bold text-blue-800">42</div>
    <div className="text-sm text-gray-600">Metric Name</div>
  </div>
</div>
```

### Common Pitfalls to Avoid

❌ Using arbitrary Tailwind values like `w-[347px]` - use standard scale
❌ Mixing measurement units inconsistently
❌ Over-complicating layouts with nested grids
❌ Forgetting mobile responsiveness
❌ Using too many different colors (stick to 2-3 color families)
❌ Walls of text without visual breaks
❌ Missing hover states on interactive elements
❌ Inconsistent spacing between sections

### Adaptive Approach

**For complex applications (games, simulations)**
- Prioritize functionality over visual flair
- Simple, functional UI that doesn't interfere
- Performance optimization

**For presentations/marketing**
- Bold, eye-catching design
- Generous use of color and gradients
- Micro-interactions and animations
- "Wow factor" visual elements

**For data/analysis**
- Clean, minimal design
- Focus on clarity and readability
- Charts and visualizations as focal points
- Subtle color coding for categories

---

## Template Structure

When creating a new artifact, start with this mental model:
1. Choose the purpose (presentation/app/document)
2. Select a color scheme (2-3 colors)
3. Plan the layout (header/content/footer)
4. Build component structure
5. Add content with hierarchy
6. Polish with spacing, shadows, hover effects
7. Test responsiveness

Remember: Only return the react code, no other text or comments.

Example:
```jsx
<div className="bg-white rounded-lg shadow-lg p-6 hover:shadow-xl transition-shadow">
  <h2 className="text-2xl font-bold text-blue-800 mb-4 flex items-center">
    <span className="text-3xl mr-3">🎯</span>
    Section Title
  </h2>
</div>
```
"""


def get_make_react_slide_prompt(content: str) -> str:
    """Generate a prompt for making a React slide"""

    return prompt_to_react_slide.format(content=content)


prompt_react_to_pptx = """\
Convert this React/HTML slide to python-pptx code:

{html_code}

Requirements:
- Use python-pptx library
- Create a blank slide layout (index 6)
- Map h1 → Title textbox at top
- Map ul/li → Bullet points
- Map img → Pictures
- Extract and apply colors, fonts, sizes
- Return complete, executable Python code
- Save the presentation in the current directory with the name "presentation.pptx"
"""


def get_react_to_pptx_prompt(react_html_code: str) -> str:
    """Generate a prompt for converting React/HTML code to python-pptx code"""

    return prompt_react_to_pptx.format(html_code=react_html_code)


# def react_to_pptx(react_html_code):
#     model = ChatOpenAI(model="gpt-4.1")
#     try:
#         response = model.invoke(
#             [{"role": "user", "content": prompt.format(html_code=react_html_code)}]
#         )
#         pptx_code = response.content
#     except Exception as e_prompt:
#         return f"Error generating PowerPoint code: {e_prompt}"
#     try:
#         exec(pptx_code)
#     except Exception as e_state:
#         return f"Error executing PowerPoint code: {e_state}"
#     return "Presentation created successfully in the directory: {pptx_path}"


# react_example = """\
# import React from 'react';

# export default function HNSWTakeaways() {
#   return (
#     <div className="w-full h-screen bg-gradient-to-br from-purple-50 to-blue-50 p-12 flex flex-col">
#       {/* Header */}
#       <div className="mb-8">
#         <h1 className="text-5xl font-bold text-purple-900 mb-2">
#           HNSW: Key Takeaways
#         </h1>
#         <div className="h-1 w-32 bg-gradient-to-r from-purple-600 to-blue-600"></div>
#       </div>

#       {/* Content Grid */}
#       <div className="grid grid-cols-2 gap-6 flex-1">
#         {/* When to Use */}
#         <div className="bg-white rounded-lg shadow-lg p-6">
#           <h2 className="text-2xl font-bold text-purple-800 mb-4 flex items-center">
#             <span className="text-3xl mr-3">📊</span>
#             When to Use HNSW
#           </h2>
#           <ul className="space-y-2 text-gray-700">
#             <li className="flex items-start">
#               <span className="text-purple-600 mr-2">•</span>
#               <span><strong>&lt;1K-5K vectors (3072-dim):</strong> Brute force may still be faster</span>
#             </li>
#             <li className="flex items-start">
#               <span className="text-purple-600 mr-2">•</span>
#               <span><strong>5K-100K vectors:</strong> HNSW shows clear advantages</span>
#             </li>
#             <li className="flex items-start">
#               <span className="text-purple-600 mr-2">•</span>
#               <span><strong>100K+ vectors:</strong> HNSW essential—brute force impractical</span>
#             </li>
#             <li className="flex items-start">
#               <span className="text-purple-600 mr-2">•</span>
#               <span>High dimensionality (1536, 3072, 4096) favors HNSW earlier</span>
#             </li>
#           </ul>
#         </div>

#         {/* Determinism & Performance */}
#         <div className="bg-white rounded-lg shadow-lg p-6">
#           <h2 className="text-2xl font-bold text-blue-800 mb-4 flex items-center">
#             <span className="text-3xl mr-3">⚡</span>
#             Determinism & Performance
#           </h2>
#           <ul className="space-y-2 text-gray-700">
#             <li className="flex items-start">
#               <span className="text-blue-600 mr-2">•</span>
#               <span><strong>Construction:</strong> Non-deterministic (random layer assignment)</span>
#             </li>
#             <li className="flex items-start">
#               <span className="text-blue-600 mr-2">•</span>
#               <span><strong>Search:</strong> Deterministic given a fixed index</span>
#             </li>
#             <li className="flex items-start">
#               <span className="text-blue-600 mr-2">•</span>
#               <span><strong>Time complexity:</strong> O(log N) vs O(N) brute force</span>
#             </li>
#             <li className="flex items-start">
#               <span className="text-blue-600 mr-2">•</span>
#               <span><strong>Memory:</strong> 1.5-3x raw data (12KB/vector → 18-36KB total)</span>
#             </li>
#           </ul>
#         </div>

#         {/* Accuracy & Trade-offs */}
#         <div className="bg-white rounded-lg shadow-lg p-6">
#           <h2 className="text-2xl font-bold text-green-800 mb-4 flex items-center">
#             <span className="text-3xl mr-3">🎯</span>
#             Accuracy & Trade-offs
#           </h2>
#           <ul className="space-y-2 text-gray-700">
#             <li className="flex items-start">
#               <span className="text-green-600 mr-2">•</span>
#               <span><strong>Approximate:</strong> 95-99%+ recall, not exact nearest neighbors</span>
#             </li>
#             <li className="flex items-start">
#               <span className="text-green-600 mr-2">•</span>
#               <span><strong>Tunable:</strong> Balance recall vs speed with ef_search, M parameters</span>
#             </li>
#             <li className="flex items-start">
#               <span className="text-green-600 mr-2">•</span>
#               <span><strong>Dynamic updates:</strong> Supports insertions/deletions after build</span>
#             </li>
#             <li className="flex items-start">
#               <span className="text-green-600 mr-2">•</span>
#               <span><strong>Build time:</strong> One-time cost, minutes to hours for millions</span>
#             </li>
#           </ul>
#         </div>

#         {/* Use Cases & Comparison */}
#         <div className="bg-white rounded-lg shadow-lg p-6">
#           <h2 className="text-2xl font-bold text-orange-800 mb-4 flex items-center">
#             <span className="text-3xl mr-3">🚀</span>
#             Modern Use Cases
#           </h2>
#           <ul className="space-y-2 text-gray-700">
#             <li className="flex items-start">
#               <span className="text-orange-600 mr-2">•</span>
#               <span><strong>RAG systems:</strong> Semantic search over embeddings</span>
#             </li>
#             <li className="flex items-start">
#               <span className="text-orange-600 mr-2">•</span>
#               <span><strong>Image similarity:</strong> CLIP, vision transformer embeddings</span>
#             </li>
#             <li className="flex items-start">
#               <span className="text-orange-600 mr-2">•</span>
#               <span><strong>Recommendations:</strong> Million+ item catalogs</span>
#             </li>
#             <li className="flex items-start">
#               <span className="text-orange-600 mr-2">•</span>
#               <span><strong>Production scale:</strong> 10M-1B+ vectors routinely handled</span>
#             </li>
#           </ul>
#         </div>
#       </div>

#       {/* Bottom Insight */}
#       <div className="mt-6 bg-gradient-to-r from-purple-600 to-blue-600 rounded-lg p-4 text-white">
#         <p className="text-center text-lg">
#           <strong>Core Insight:</strong> HNSW's hierarchical structure mirrors
#           intuitive search—upper layers as "highways" between clusters,
#           lower layers as "local streets." Critical for high-dimensional vectors
#           where each distance calculation is expensive.
#         </p>
#       </div>
#     </div>
#   );
# }
# """
