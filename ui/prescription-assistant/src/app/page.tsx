"use client";

import { PrescriptionsCard } from "@/components/prescriptions";
import { WeatherCard } from "@/components/weather";
import { AgentState } from "@/lib/types";
import {
  useCoAgent,
  useDefaultTool,
  useFrontendTool,
  useHumanInTheLoop,
  useRenderToolCall,
} from "@copilotkit/react-core";
import { CopilotKitCSSProperties, CopilotSidebar } from "@copilotkit/react-ui";
import { useState } from "react";

export default function CopilotKitPage() {
  const [themeColor, setThemeColor] = useState("#3b82f6"); // Medium Blue (Blue-500)

  // 🪁 Frontend Actions: https://docs.copilotkit.ai/adk/frontend-actions
  useFrontendTool({
    name: "setThemeColor",
    parameters: [
      {
        name: "themeColor",
        description: "The theme color to set. Make sure to pick nice colors.",
        required: true,
      },
    ],
    handler({ themeColor }) {
      setThemeColor(themeColor);
    },
  });

  return (
    <main
      style={
        { "--copilot-kit-primary-color": themeColor } as CopilotKitCSSProperties
      }
    >
      <CopilotSidebar
        disableSystemMessage={true}
        clickOutsideToClose={false}
        defaultOpen={true}
        imageUploadsEnabled={true}
        inputFileAccept="image/*"
        icons={{
          uploadIcon: (
            <div className="flex items-center gap-2 px-3 py-1.5 bg-white/20 hover:bg-white/30 rounded-full border border-white/30 transition-all cursor-pointer">
              <span className="text-lg">📸</span>
              <span className="text-xs font-semibold whitespace-nowrap">New prescription</span>
            </div>
          ),
        }}
        labels={{
          title: "Prescription Assistant",
          initial: "👋 Hi! I'm your Prescription Assistant. How can I help you today?",
          placeholder: "Type a message or upload an image...",
        }}
        suggestions={[
          {
            title: "Add new prescription",
            message: "I want to add a new prescription.",
          },
          {
            title: "Check my current prescriptions",
            message: "What are my current prescriptions?",
          },
          {
            title: "Check possible side effects",
            message: "What are the possible side effects for my prescriptions?",
          },
        ]}
      >
        <YourMainContent themeColor={themeColor} />
      </CopilotSidebar>
    </main>
  );
}

function YourMainContent({ themeColor }: { themeColor: string }) {
  // 🪁 Shared State: https://docs.copilotkit.ai/adk/shared-state
  const { state, setState } = useCoAgent<AgentState>({
    name: "my_agent",
    initialState: {
      prescriptions: [
        "Aspirin - 100mg - Daily",
      ],
    },
  });

  //🪁 Generative UI: https://docs.copilotkit.ai/adk/generative-ui
  useRenderToolCall(
    {
      name: "get_weather",
      description: "Get the weather for a given location.",
      parameters: [{ name: "location", type: "string", required: true }],
      render: ({ args, result }) => {
        return <WeatherCard location={args.location} themeColor={themeColor} />;
      },
    },
    [themeColor],
  );

  return (
    <div
      style={{ backgroundColor: themeColor }}
      className="h-screen flex justify-center items-center flex-col transition-colors duration-300"
    >
      <PrescriptionsCard state={state} setState={setState} />
    </div>
  );
}
