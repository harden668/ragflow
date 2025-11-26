import { loader } from '@monaco-editor/react';

// Configure Monaco editor to use the correct path for workers
// This prevents the "Failed to parse URL from /vs/language/json/jsonWorker.js" error
export function configureMonacoEditor() {
  // Only configure if not already configured
  if (typeof window !== 'undefined' && !(window as any).monacoConfigured) {
    loader.config({
      paths: {
        vs: `${window.location.origin}/vs`,
      },
      'vs/nls': {
        availableLanguages: {
          '*': 'zh-cn',
        },
      },
    });

    // Mark as configured to prevent duplicate configuration
    (window as any).monacoConfigured = true;
  }
}
