const pptxgen = require("pptxgenjs");

const pres = new pptxgen();
pres.layout = "LAYOUT_16x9";
pres.author = "Claude Code";
pres.title = "Claude Code Introduction";

// Color palette: Charcoal Minimal with teal accent
const C = {
  dark: "1A1A2E",
  navy: "16213E",
  teal: "0F3460",
  accent: "00ADB5",
  accentLight: "39A2DB",
  white: "FFFFFF",
  offWhite: "F5F5F5",
  lightGray: "E4E4E4",
  gray: "999999",
  text: "2D2D2D",
  textLight: "6B7280",
};

const makeShadow = () => ({
  type: "outer",
  blur: 8,
  offset: 3,
  angle: 135,
  color: "000000",
  opacity: 0.12,
});

// ============ SLIDE 1: Cover ============
let s1 = pres.addSlide();
s1.background = { color: C.dark };

// Decorative shapes
s1.addShape(pres.shapes.RECTANGLE, {
  x: 0, y: 0, w: 10, h: 0.06, fill: { color: C.accent },
});
s1.addShape(pres.shapes.RECTANGLE, {
  x: 0, y: 5.565, w: 10, h: 0.06, fill: { color: C.accent },
});

// Left accent bar
s1.addShape(pres.shapes.RECTANGLE, {
  x: 0.8, y: 1.6, w: 0.06, h: 2.4, fill: { color: C.accent },
});

// Title area
s1.addText("Claude Code", {
  x: 1.2, y: 1.5, w: 7.5, h: 1.2,
  fontSize: 48, fontFace: "Arial Black",
  color: C.white, margin: 0,
});
s1.addText("Anthropic Official CLI for Claude", {
  x: 1.2, y: 2.65, w: 7.5, h: 0.6,
  fontSize: 20, fontFace: "Calibri",
  color: C.accent, margin: 0,
});
s1.addText("Your AI-Powered Software Engineering Assistant", {
  x: 1.2, y: 3.2, w: 7.5, h: 0.5,
  fontSize: 14, fontFace: "Calibri",
  color: C.gray, margin: 0,
});

// Bottom info
s1.addText("Powered by Claude  |  claude.ai/code", {
  x: 1.2, y: 4.5, w: 7, h: 0.4,
  fontSize: 12, fontFace: "Calibri",
  color: C.textLight, margin: 0,
});

// ============ SLIDE 2: What is Claude Code ============
let s2 = pres.addSlide();
s2.background = { color: C.offWhite };

s2.addShape(pres.shapes.RECTANGLE, {
  x: 0, y: 0, w: 10, h: 0.9, fill: { color: C.dark },
});
s2.addText("What is Claude Code?", {
  x: 0.8, y: 0.15, w: 8, h: 0.6,
  fontSize: 28, fontFace: "Arial Black",
  color: C.white, margin: 0,
});

// Main description card
s2.addShape(pres.shapes.RECTANGLE, {
  x: 0.8, y: 1.3, w: 8.4, h: 1.2,
  fill: { color: C.white },
  shadow: makeShadow(),
});
s2.addText("Claude Code is an interactive command-line tool that brings Claude directly into your terminal. It reads your codebase, understands context, and helps you build, debug, and ship software faster.", {
  x: 1.1, y: 1.35, w: 7.8, h: 1.1,
  fontSize: 14, fontFace: "Calibri",
  color: C.text, margin: 0, valign: "middle",
});

// Three feature cards
const features = [
  { title: "Agentic Coding", desc: "Autonomously reads files, writes code, runs commands, and iterates on solutions.", accent: C.accent },
  { title: "Context Aware", desc: "Understands your entire project structure, dependencies, and coding patterns.", accent: C.accentLight },
  { title: "Multi-Modal", desc: "Reads images, screenshots, and diagrams to understand visual requirements.", accent: C.teal },
];

features.forEach((f, i) => {
  const xPos = 0.8 + i * 2.9;
  s2.addShape(pres.shapes.RECTANGLE, {
    x: xPos, y: 2.85, w: 2.6, h: 2.2,
    fill: { color: C.white },
    shadow: makeShadow(),
  });
  s2.addShape(pres.shapes.RECTANGLE, {
    x: xPos, y: 2.85, w: 2.6, h: 0.06,
    fill: { color: f.accent },
  });
  s2.addText(f.title, {
    x: xPos + 0.2, y: 3.1, w: 2.2, h: 0.5,
    fontSize: 16, fontFace: "Arial", bold: true,
    color: C.text, margin: 0,
  });
  s2.addText(f.desc, {
    x: xPos + 0.2, y: 3.6, w: 2.2, h: 1.2,
    fontSize: 12, fontFace: "Calibri",
    color: C.textLight, margin: 0,
  });
});

// ============ SLIDE 3: Core Capabilities ============
let s3 = pres.addSlide();
s3.background = { color: C.offWhite };

s3.addShape(pres.shapes.RECTANGLE, {
  x: 0, y: 0, w: 10, h: 0.9, fill: { color: C.dark },
});
s3.addText("Core Capabilities", {
  x: 0.8, y: 0.15, w: 8, h: 0.6,
  fontSize: 28, fontFace: "Arial Black",
  color: C.white, margin: 0,
});

const capabilities = [
  { num: "01", title: "Code Writing", desc: "Generate, modify, and refactor code across multiple files and languages with precision." },
  { num: "02", title: "Code Search", desc: "Find files, symbols, and patterns across your entire codebase instantly using glob and grep." },
  { num: "03", title: "Debugging", desc: "Diagnose errors, trace root causes, and apply fixes by analyzing logs and stack traces." },
  { num: "04", title: "Testing", desc: "Write and run tests, analyze failures, and iterate until all tests pass." },
  { num: "05", title: "Git Operations", desc: "Create commits, branches, pull requests, and manage your git workflow seamlessly." },
  { num: "06", title: "System Commands", desc: "Execute shell commands, install packages, build projects, and manage infrastructure." },
];

capabilities.forEach((cap, i) => {
  const col = i % 3;
  const row = Math.floor(i / 3);
  const xPos = 0.8 + col * 2.9;
  const yPos = 1.2 + row * 2.15;

  s3.addShape(pres.shapes.RECTANGLE, {
    x: xPos, y: yPos, w: 2.6, h: 1.85,
    fill: { color: C.white },
    shadow: makeShadow(),
  });

  s3.addText(cap.num, {
    x: xPos + 0.15, y: yPos + 0.1, w: 0.6, h: 0.4,
    fontSize: 22, fontFace: "Arial Black",
    color: C.accent, margin: 0,
  });

  s3.addText(cap.title, {
    x: xPos + 0.15, y: yPos + 0.55, w: 2.3, h: 0.35,
    fontSize: 14, fontFace: "Arial", bold: true,
    color: C.text, margin: 0,
  });

  s3.addText(cap.desc, {
    x: xPos + 0.15, y: yPos + 0.9, w: 2.3, h: 0.8,
    fontSize: 11, fontFace: "Calibri",
    color: C.textLight, margin: 0,
  });
});

// ============ SLIDE 4: How It Works ============
let s4 = pres.addSlide();
s4.background = { color: C.offWhite };

s4.addShape(pres.shapes.RECTANGLE, {
  x: 0, y: 0, w: 10, h: 0.9, fill: { color: C.dark },
});
s4.addText("How It Works", {
  x: 0.8, y: 0.15, w: 8, h: 0.6,
  fontSize: 28, fontFace: "Arial Black",
  color: C.white, margin: 0,
});

// Three-step flow
const steps = [
  { num: "1", title: "You Describe", desc: "Type your request in natural language directly in the terminal. Be it a bug fix, new feature, or a question.", color: C.accent },
  { num: "2", title: "Claude Acts", desc: "Reads relevant files, searches the codebase, runs commands, and writes code using a suite of powerful tools.", color: C.accentLight },
  { num: "3", title: "You Review", desc: "Review the proposed changes, approve tool usage, and iterate until the result meets your expectations.", color: C.teal },
];

steps.forEach((step, i) => {
  const xPos = 0.8 + i * 3.0;

  // Card
  s4.addShape(pres.shapes.RECTANGLE, {
    x: xPos, y: 1.3, w: 2.7, h: 3.2,
    fill: { color: C.white },
    shadow: makeShadow(),
  });

  // Number circle
  s4.addShape(pres.shapes.OVAL, {
    x: xPos + 0.95, y: 1.55, w: 0.8, h: 0.8,
    fill: { color: step.color },
  });
  s4.addText(step.num, {
    x: xPos + 0.95, y: 1.55, w: 0.8, h: 0.8,
    fontSize: 28, fontFace: "Arial Black",
    color: C.white, align: "center", valign: "middle", margin: 0,
  });

  s4.addText(step.title, {
    x: xPos + 0.2, y: 2.5, w: 2.3, h: 0.4,
    fontSize: 16, fontFace: "Arial", bold: true,
    color: C.text, align: "center", margin: 0,
  });

  s4.addText(step.desc, {
    x: xPos + 0.2, y: 2.95, w: 2.3, h: 1.3,
    fontSize: 12, fontFace: "Calibri",
    color: C.textLight, align: "center", margin: 0,
  });

  // Arrow between cards
  if (i < 2) {
    s4.addShape(pres.shapes.LINE, {
      x: xPos + 2.7, y: 2.35, w: 0.3, h: 0,
      line: { color: C.accent, width: 2 },
    });
  }
});

// Agent mode note
s4.addShape(pres.shapes.RECTANGLE, {
  x: 0.8, y: 4.7, w: 8.4, h: 0.5,
  fill: { color: C.dark },
});
s4.addText("Agent Mode: Spawn specialized sub-agents for parallel task execution and complex multi-step workflows.", {
  x: 1.0, y: 4.7, w: 8.0, h: 0.5,
  fontSize: 12, fontFace: "Calibri",
  color: C.accent, valign: "middle", margin: 0,
});

// ============ SLIDE 5: Supported Environments ============
let s5 = pres.addSlide();
s5.background = { color: C.offWhite };

s5.addShape(pres.shapes.RECTANGLE, {
  x: 0, y: 0, w: 10, h: 0.9, fill: { color: C.dark },
});
s5.addText("Supported Environments", {
  x: 0.8, y: 0.15, w: 8, h: 0.6,
  fontSize: 28, fontFace: "Arial Black",
  color: C.white, margin: 0,
});

const envs = [
  { title: "Terminal / CLI", desc: "Full-featured interactive REPL in your terminal. Works on macOS, Linux, and Windows (WSL/Git Bash).", icon: ">" },
  { title: "VS Code Extension", desc: "Integrated experience within Visual Studio Code. Inline suggestions and side-by-side code review.", icon: "{" },
  { title: "JetBrains Plugin", desc: "Deep integration with IntelliJ, PyCharm, WebStorm, and other JetBrains IDEs.", icon: "#" },
  { title: "Desktop App", desc: "Standalone desktop application for macOS and Windows with a native feel.", icon: "=" },
  { title: "Web App", desc: "Access Claude Code directly from claude.ai/code in your browser, anywhere.", icon: "/" },
  { title: "API / SDK", desc: "Build custom agents and workflows using the Anthropic SDK and Claude Agent SDK.", icon: "+" },
];

envs.forEach((env, i) => {
  const col = i % 3;
  const row = Math.floor(i / 3);
  const xPos = 0.8 + col * 2.9;
  const yPos = 1.2 + row * 2.15;

  s5.addShape(pres.shapes.RECTANGLE, {
    x: xPos, y: yPos, w: 2.6, h: 1.85,
    fill: { color: C.white },
    shadow: makeShadow(),
  });

  // Icon-like box
  s5.addShape(pres.shapes.RECTANGLE, {
    x: xPos + 0.15, y: yPos + 0.15, w: 0.5, h: 0.4,
    fill: { color: C.dark },
  });
  s5.addText(env.icon, {
    x: xPos + 0.15, y: yPos + 0.15, w: 0.5, h: 0.4,
    fontSize: 16, fontFace: "Consolas",
    color: C.accent, align: "center", valign: "middle", margin: 0,
  });

  s5.addText(env.title, {
    x: xPos + 0.75, y: yPos + 0.15, w: 1.7, h: 0.4,
    fontSize: 14, fontFace: "Arial", bold: true,
    color: C.text, valign: "middle", margin: 0,
  });

  s5.addText(env.desc, {
    x: xPos + 0.15, y: yPos + 0.7, w: 2.3, h: 1.0,
    fontSize: 11, fontFace: "Calibri",
    color: C.textLight, margin: 0,
  });
});

// ============ SLIDE 6: Closing ============
let s6 = pres.addSlide();
s6.background = { color: C.dark };

s6.addShape(pres.shapes.RECTANGLE, {
  x: 0, y: 0, w: 10, h: 0.06, fill: { color: C.accent },
});
s6.addShape(pres.shapes.RECTANGLE, {
  x: 0, y: 5.565, w: 10, h: 0.06, fill: { color: C.accent },
});

s6.addText("Start Building with", {
  x: 1, y: 1.3, w: 8, h: 0.6,
  fontSize: 22, fontFace: "Calibri",
  color: C.gray, align: "center", margin: 0,
});
s6.addText("Claude Code", {
  x: 1, y: 1.85, w: 8, h: 1.0,
  fontSize: 52, fontFace: "Arial Black",
  color: C.white, align: "center", margin: 0,
});

s6.addShape(pres.shapes.RECTANGLE, {
  x: 4.2, y: 3.0, w: 1.6, h: 0.04, fill: { color: C.accent },
});

s6.addText("Install:  npm install -g @anthropic-ai/claude-code", {
  x: 1.5, y: 3.3, w: 7, h: 0.5,
  fontSize: 16, fontFace: "Consolas",
  color: C.accent, align: "center", margin: 0,
});

s6.addText("Learn more at claude.ai/code", {
  x: 1.5, y: 3.9, w: 7, h: 0.4,
  fontSize: 14, fontFace: "Calibri",
  color: C.textLight, align: "center", margin: 0,
});

pres.writeFile({ fileName: "P:\\github_my_repo\\repo_template\\introduction.pptx" })
  .then(() => console.log("PPTX created successfully!"))
  .catch(err => console.error("Error:", err));
