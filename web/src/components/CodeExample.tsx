import { CopyButton } from "./CopyButton";
import { Reveal } from "./Reveal";
import { Section } from "./Section";

const RAW = `from aegize import guarded_tool

@guarded_tool(
    tool_name="email",
    operation="send",
    risk_level="high",
)
def send_email(...):
    ...`;

// GitHub-dark inspired token colors
const C = {
  kw: "#ff7b72",
  deco: "#d2a8ff",
  fn: "#d2a8ff",
  str: "#a5d6ff",
  punc: "#8b949e",
  fg: "#e6edf3",
};

const K = ({ children }: { children: string }) => <span style={{ color: C.kw }}>{children}</span>;
const S = ({ children }: { children: string }) => <span style={{ color: C.str }}>{children}</span>;
const P = ({ children }: { children: string }) => <span style={{ color: C.punc }}>{children}</span>;

export function CodeExample() {
  return (
    <Section
      id="code"
      eyebrow="Developer-first"
      title="Govern any tool in three lines."
      intro="Wrap a function with a decorator. Aegize attaches identity, evaluates policy, gates for approval, and records the result — before your code runs."
    >
      <Reveal className="mx-auto mt-12 max-w-2xl" delay={80}>
        <div className="overflow-hidden rounded-xl border border-border-strong bg-[#0d1117] shadow-2xl shadow-black/40">
          <div className="flex items-center justify-between border-b border-border px-4 py-2.5">
            <div className="flex items-center gap-2">
              <span className="h-3 w-3 rounded-full bg-[#ff5f56]" />
              <span className="h-3 w-3 rounded-full bg-[#ffbd2e]" />
              <span className="h-3 w-3 rounded-full bg-[#27c93f]" />
              <span className="ml-2 font-mono text-xs text-faint">tools.py</span>
            </div>
            <CopyButton text={RAW} />
          </div>

          <pre className="overflow-x-auto px-5 py-5 font-mono text-[0.86rem] leading-7">
            <code style={{ color: C.fg }}>
              <K>from</K> aegize <K>import</K> guarded_tool{"\n"}
              {"\n"}
              <span style={{ color: C.deco }}>@guarded_tool</span>
              <P>(</P>
              {"\n"}
              {"    "}tool_name<P>=</P>
              <S>&quot;email&quot;</S>
              <P>,</P>
              {"\n"}
              {"    "}operation<P>=</P>
              <S>&quot;send&quot;</S>
              <P>,</P>
              {"\n"}
              {"    "}risk_level<P>=</P>
              <S>&quot;high&quot;</S>
              <P>,</P>
              {"\n"}
              <P>)</P>
              {"\n"}
              <K>def</K> <span style={{ color: C.fn }}>send_email</span>
              <P>(...):</P>
              {"\n"}
              {"    "}
              <P>...</P>
            </code>
          </pre>
        </div>
      </Reveal>
    </Section>
  );
}
