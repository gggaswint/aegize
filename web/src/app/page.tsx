import { Architecture } from "@/components/Architecture";
import { CodeExample } from "@/components/CodeExample";
import { DemoSection } from "@/components/DemoSection";
import { Features } from "@/components/Features";
import { Footer } from "@/components/Footer";
import { Hero } from "@/components/Hero";
import { Nav } from "@/components/Nav";
import { OpenSource } from "@/components/OpenSource";
import { RuntimeSection } from "@/components/RuntimeSection";
import { TryTheRuntime } from "@/components/TryTheRuntime";
import { Why } from "@/components/Why";

function Divider() {
  return <div className="hairline mx-auto h-px w-full max-w-6xl" />;
}

export default function Home() {
  return (
    <>
      <Nav />
      <main id="main">
        <Hero />
        <RuntimeSection />
        <Divider />
        <DemoSection />
        <Divider />
        <TryTheRuntime />
        <Divider />
        <Why />
        <Features />
        <Divider />
        <CodeExample />
        <Architecture />
        <OpenSource />
      </main>
      <Footer />
    </>
  );
}
