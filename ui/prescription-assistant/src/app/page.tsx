"use client";

import { useRef, useState, useCallback, useEffect } from "react";
import {
  CopilotChat,
  useAgent,
  useCopilotKit,
} from "@copilotkit/react-core/v2";
import "@copilotkit/react-core/v2/styles.css";
import { ToolCallRenderer } from "./components/ToolCallRenderer";
import { randomUUID } from "@copilotkit/shared";

/**
 * Content part types for AG-UI multimodal messages
 */
type TextContent = {
  type: "text";
  text: string;
};

type BinaryContent = {
  type: "binary";
  mimeType: string;
  data: string;
  filename?: string;
};

type ContentPart = TextContent | BinaryContent;

// Sample-specific configuration
const AGENT_ID = "default";
const HEADER_TITLE = "Medical Prescription Assistant";
const HEADER_SUBTITLE = "An AI-powered medical prescription assistant- gHacks2026 - Argo Team";

export default function Page() {
  const [selectedFiles, setSelectedFiles] = useState<string[]>([]);
  const [inputValue, setInputValue] = useState("");
  const fileInputRef = useRef<HTMLInputElement>(null);
  const selectedFilesRef = useRef<string[]>([]);
  const { copilotkit } = useCopilotKit();

  // CUSTOMIZE: Change agentId to match your agent name in agent.yaml
  const { agent } = useAgent({ agentId: AGENT_ID });

  // Keep ref in sync with state for use in callbacks
  useEffect(() => {
    selectedFilesRef.current = selectedFiles;
  }, [selectedFiles]);

  // Handle file selection
  const handleFileSelect = useCallback(
    async (event: React.ChangeEvent<HTMLInputElement>) => {

      // UPLOAD file to cloud storage
      const files = event.target.files;
      if (!files || files.length === 0) return;

      console.log(`[FileSelect] Starting upload for ${files.length} files`);

      const filePromises = Array.from(files).map(async (file) => {
        console.log(`[FileSelect] Uploading file: ${file.name} (${file.type}, ${file.size} bytes)`);
        const formData = new FormData();
        formData.append("file", file);

        try {
          const response = await fetch("https://mpa-runtime-969700488226.us-central1.run.app/upload", {
            method: "POST",
            body: formData,
          });

          if (!response.ok) {
            const errorText = await response.text();
            console.error(`[FileSelect] Upload failed for ${file.name}:`, response.status, errorText);
            return null;
          }

          const data = await response.json();
          console.log(`[FileSelect] Successfully uploaded ${file.name}. Result URL:`, data.filename);
          return data.filename;
        } catch (error) {
          console.error(`[FileSelect] Error uploading ${file.name}:`, error);
          return null;
        }
      });

      const loadedFiles = (await Promise.all(filePromises)).filter(
        (f): f is string => f !== null
      );

      console.log(`[FileSelect] Completed uploads. Successfully uploaded ${loadedFiles.length} out of ${files.length} files.`);
      setSelectedFiles((prev) => [...prev, ...loadedFiles]);

      if (event.target) {
        event.target.value = "";
      }
    },
    []
  );

  // Handle clipboard paste for images
  useEffect(() => {
    const handlePaste = async (e: ClipboardEvent) => {
      const items = Array.from(e.clipboardData?.items || []);
      const imageItems = items.filter((item) => item.type.startsWith("image/"));
      if (imageItems.length === 0) return;

      console.log(`[Paste] Detected ${imageItems.length} pasted images`);
      e.preventDefault();

      const imagePromises = imageItems.map(async (item) => {
        const file = item.getAsFile();
        if (!file) return null;

        console.log(`[Paste] Uploading pasted image: ${file.name} (${file.type})`);
        const formData = new FormData();
        formData.append("file", file);

        try {
          const response = await fetch("https://mpa-runtime-969700488226.us-central1.run.app/upload", {
            method: "POST",
            body: formData,
          });

          if (!response.ok) {
            const errorText = await response.text();
            console.error(`[Paste] Upload failed:`, response.status, errorText);
            return null;
          }

          const data = await response.json();
          console.log(`[Paste] Successfully uploaded pasted image. Result URL:`, data.filename);
          return data.filename;
        } catch (error) {
          console.error(`[Paste] Error uploading pasted image:`, error);
          return null;
        }
      });

      const loadedImages = (await Promise.all(imagePromises)).filter(
        (img): img is string => img !== null
      );

      console.log(`[Paste] Completed uploads. Successfully uploaded ${loadedImages.length} images.`);
      setSelectedFiles((prev) => [...prev, ...loadedImages]);
    };

    document.addEventListener("paste", handlePaste);
    return () => document.removeEventListener("paste", handlePaste);
  }, []);

  // Remove a file from queue
  const removeFile = useCallback((index: number) => {
    const fileToRemove = selectedFiles[index];
    console.log(`[RemoveFile] Removing file at index ${index}:`, fileToRemove);
    setSelectedFiles((prev) => prev.filter((_, i) => i !== index));
  }, [selectedFiles]);

  // Handle message submission - ALWAYS use our handler for full control
  const handleSubmitMessage = useCallback(
    async (text: string) => {

      console.log("[SubmitMessage] Attempting to submit message:", { text, fileCount: selectedFilesRef.current.length });

      if (!agent) {
        console.error("[SubmitMessage] No agent available");
        return;
      }

      const currentFiles = selectedFilesRef.current;
      const hasText = text.trim().length > 0;
      const hasFiles = currentFiles.length > 0;

      if (!hasText && !hasFiles) {
        console.warn("[SubmitMessage] Empty message and no files, ignoring submission");
        return;
      }

      // Build content - use array format when files present, string otherwise
      let content: string | ContentPart[];

      if (hasFiles) {
        const contentParts: ContentPart[] = [];

        if (hasText) {
          contentParts.push({ type: "text", text: text.trim() });
        }

        for (const fileUrl of currentFiles) {
          contentParts.push({
            type: "text",
            text: fileUrl,
          });
        }

        content = contentParts;

        console.log("[SubmitMessage] Built multimodal content:", JSON.stringify(content, null, 2));
      } else {
        content = text.trim();
        console.log("[SubmitMessage] Built text-only content:", content);
      }

      // Clear state
      setSelectedFiles([]);
      setInputValue("");

      // Create and send message
      const message = {
        id: randomUUID(),
        role: "user" as const,
        content,
      };

      console.log("[SubmitMessage] Adding message to agent:", message.id);
      agent.addMessage(message);

      try {
        console.log("[SubmitMessage] Running agent...");
        await copilotkit.runAgent({ agent });
        console.log("[SubmitMessage] Agent run completed successfully");
      } catch (error) {
        console.error("[SubmitMessage] Error running agent:", error);
      }
    },
    [agent, copilotkit]
  );

  // Stop generation
  const handleStop = useCallback(() => {
    console.log("[Stop] Requesting agent to stop");
    agent?.abortRun?.();
  }, [agent]);

  const messages = agent?.messages ?? [];
  const isRunning = agent?.isRunning ?? false;

  return (
    <div className="flex flex-col h-screen">
      <ToolCallRenderer />

      <header className="border-b border-zinc-200 dark:border-zinc-800 px-6 py-4 bg-white dark:bg-zinc-900">
        <h1 className="text-xl font-semibold text-zinc-900 dark:text-zinc-100">
          {HEADER_TITLE}
        </h1>
        <p className="text-sm text-zinc-500 dark:text-zinc-400">
          {HEADER_SUBTITLE}
        </p>
      </header>

      <main className="flex-1 overflow-hidden flex flex-col">
        {/* File upload queue */}
        {selectedFiles.length > 0 && (
          <div className="flex flex-wrap gap-2 p-3 border-b border-zinc-200 dark:border-zinc-700 bg-zinc-50 dark:bg-zinc-800">
            {selectedFiles.map((file, index) => (
              <div
                key={index}
                className="relative inline-block w-16 h-16 rounded-lg overflow-hidden border border-zinc-300 dark:border-zinc-600"
              >
                <div className="w-full h-full flex items-center justify-center bg-zinc-200 dark:bg-zinc-700">
                  <span className="text-xs text-zinc-600 dark:text-zinc-300 text-center px-1 break-all line-clamp-3">
                    {file.split('/').pop() || "FILE"}
                  </span>
                </div>
                <button
                  onClick={() => removeFile(index)}
                  className="absolute top-0.5 right-0.5 w-5 h-5 flex items-center justify-center bg-black/60 text-white rounded-full text-xs hover:bg-black/80"
                  aria-label="Remove file"
                >
                  x
                </button>
              </div>
            ))}
          </div>
        )}

        {/* Hidden file input */}
        <input
          type="file"
          multiple
          ref={fileInputRef}
          onChange={handleFileSelect}
          accept="image/*,application/pdf,.doc,.docx,.txt"
          className="hidden"
        />

        {/* CopilotChatView - full control over messages and input */}
        <CopilotChat.View
          className="flex-1"
          messages={messages}
          isRunning={isRunning}
          suggestions={[{
            title: "I have a doubt about my medicines",
            message: "Analyze my presciptions to solve my questions",
            isLoading: false
          },
          {
            title: "Generate the faster route to buy my medicines",
            message: "Extract the information of my prescription, seach in the inventorty and generate the fastest route to buy my medicines",
            isLoading: false
          },
          {
            title: "Generate the faster route to buy my medicines",
            message: "Extract the information of my prescription, seach in the inventorty and generate the fastest route to buy my medicines",
            isLoading: false
          }]}
          input={{
            value: inputValue,
            onChange: setInputValue,
            onSubmitMessage: handleSubmitMessage,
            onStop: handleStop,
            isRunning,
            onAddFile: () => {
              console.log("[Input] Triggering file input click");
              fileInputRef.current?.click();
            },
          }}
        />
      </main>
    </div>
  );
}
