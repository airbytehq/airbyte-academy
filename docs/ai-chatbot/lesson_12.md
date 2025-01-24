## Bonus: Create a Front End, Next.js
Duration: 0:15:00

Now that we have our chatbot working in Python, let's create a web interface using Next.js. This will give users an intuitive way to interact with our AI-powered data analysis.

The app when finished, should look something like:

[![Airbyte AI Sample](https://img.youtube.com/vi/irh42TDNTFQ/0.jpg)](https://www.youtube.com/watch?v=irh42TDNTFQ)


If you prefer, the code for the app is avaible in this  [GitHub repo](https://github.com/AkritiKeswani/ecommerce-chatbot//). To help you better navigate the app,  see the directory structure below
```
ecommerce-chatbot/
├── src/
│   ├── app/
│   │   ├── api/
│   │   │   └── chat/
│   │   │       └── route.ts         # API endpoint for chat
│   │   ├── globals.css
│   │   ├── layout.tsx
│   │   └── page.tsx                 # Main chat interface
│   ├── components/
│   │   └── ui/
│   │       ├── ChatInput.tsx        # Input component
│   │       ├── ChatMessage.tsx      # Message display component
│   │       └── theme-provider.tsx   # Theme configuration
│   ├── lib/
│   │   ├── openai.ts               # OpenAI client setup
│   │   └── supabase.ts             # Supabase client setup
│   └── types/
│       └── chat.ts                 # TypeScript interfaces
├── public/
│   └── favicon.ico
├── .env.local                      # Environment variables
├── .gitignore
├── eslint.config.mjs               # ESLint configuration
├── next.config.ts                  # Next.js configuration
├── next-env.d.ts                   # Next.js TypeScript declarations
├── package.json
├── package-lock.json
├── postcss.config.mjs              # PostCSS configuration
└── tsconfig.json                   # TypeScript configuration
```

### Step 1: Setup Next.js Project
Go ahead and create the basic app scaffolding:
```
npx create-next-app@latest ecommerce-chatbot --typescript --tailwind --eslint
cd  ecommerece-chatbot
```

**Install Dependencies**
Then install the dependencies

`npm install @supabase/supabase-js openai`

**Environment Variables**
We need a few personal keys for the app to run. You already have these from previous sections in the tutorial. We will store them in a local environment file for next.js to use.

Create `.env.local` in the root directory. 

```
NEXT_PUBLIC_SUPABASE_URL=your_supabase_url
NEXT_PUBLIC_SUPABASE_ANON_KEY=your_supabase_anon_key
OPENAI_API_KEY=your_openai_key
```
### Step 2: Create API Route 
Let's create some API routes so you app knows where to go

`(/api/chat/route.ts)`

This is the most critical part of the app, where the user's query is:

- Categorized using GPT.
- Processed to find relevant data using Supabase vector search.
- Answered intelligently by GPT based on retrieved data.
= Navigate to `app/api/chat/` and create a file named route.ts.

This is where you set up connections to Supabase and OpenAI. 

```typescript
import { NextResponse } from 'next/server';
import OpenAI from 'openai';
import { createClient } from '@supabase/supabase-js';

// Initialize Supabase client
const supabase = createClient(
  process.env.NEXT_PUBLIC_SUPABASE_URL!,
  process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!
);

// Initialize OpenAI client
const openai = new OpenAI({
  apiKey: process.env.OPENAI_API_KEY!,
});
```

This generates the embedding for the user query. 
```
// Generate embedding for the user's query
async function getQueryEmbedding(message: string) {
  const response = await openai.embeddings.create({
    model: 'text-embedding-ada-002',
    input: message,
  });
  return response.data[0].embedding;
}
```
Now, we use GPT to determine whether the query is related to customers, products, or invoices. 

```
// Categorize the user's query
async function categorizeQuery(message: string) {
  const response = await openai.chat.completions.create({
    model: 'gpt-4',
    messages: [
      {
        role: 'system',
        content: `You are an e-commerce assistant. Categorize the query into one of these categories:
        - CUSTOMER: For accounts, profiles, personal details, users
        - PRODUCT: For items, inventory, specifications, pricing
        - ORDER: For payments, invoices, orders, shipping
        Respond with just the category name.`,
      },
      { role: 'user', content: message },
    ],
    temperature: 0.3,
    max_tokens: 10,
  });
  return response.choices[0].message.content?.trim().toUpperCase();
}
```
Now, we map the category to the right Supabase function: 

```
// Match query category to Supabase function
function getSupabaseFunction(category: string) {
  const functionMap = {
    CUSTOMER: 'find_related_customer',
    PRODUCT: 'find_related_products',
    ORDER: 'find_related_invoices',
  };
  return functionMap[category];
}
```

The function from Supabase is called and retrives the relevant data. 

```
// Query Supabase for related data
async function querySupabase(functionName: string, queryEmbedding: number[]) {
  const { data, error } = await supabase.rpc(functionName, {
    question_vector: queryEmbedding,
  });
  if (error) throw new Error(`Supabase error: ${error.message}`);
  return data;
}
```
GPT generates a final response. 
```
// Generate a meaningful response using GPT
async function generateGPTResponse(message: string, context: string) {
  const response = await openai.chat.completions.create({
    model: 'gpt-4',
    messages: [
      {
        role: 'system',
        content: 'You are an intelligent assistant. Use the provided context to answer the query clearly and concisely.',
      },
      {
        role: 'user',
        content: `Question: ${message}\n\nContext:\n${context}`,
      },
    ],
    temperature: 0.3,
    max_tokens: 300,
  });
  return response.choices[0].message.content;
}
```

Lastly, we can consolidate all of this into a POST function that is the final request: 

```
export async function POST(request: Request) {
  try {
    const { message } = await request.json();
    console.log('Incoming message:', message);

    // Step 1: Get embedding for the query
    const queryEmbedding = await getQueryEmbedding(message);

    // Step 2: Categorize the query
    const category = await categorizeQuery(message);
    console.log('Detected category:', category);

    if (!['CUSTOMER', 'PRODUCT', 'ORDER'].includes(category)) {
      return NextResponse.json({
        content: 'Please ask about customers, products, or orders.',
      });
    }

    // Step 3: Match category to Supabase function
    const functionName = getSupabaseFunction(category);
    console.log('Matched function:', functionName);

    // Step 4: Query Supabase
    const documents = await querySupabase(functionName, queryEmbedding);
    const context = documents?.map((doc: any) => doc.document_content).join('\n') || 'No relevant data found.';

    // Step 5: Generate GPT response
    const response = await generateGPTResponse(message, context);

    return NextResponse.json({ content: response });
  } catch (error: any) {
    console.error('Error:', error.message);
    return NextResponse.json({ error: 'Something went wrong.' }, { status: 500 });
  }
}
```
### Step 3: Entry Point for App
Once you complete the route, you will have to add to `page.tsx` as that is your main entry point:

```
'use client';

import { useState } from 'react';
import ChatInput from './components/ChatInput';
import ChatMessage from './components/ChatMessage';

interface Message {
  role: 'user' | 'assistant';
  content: string;
}

export default function Chat() {
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState('');
  const [isLoading, setIsLoading] = useState(false);

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    if (!input.trim()) return;

    const userMessage = { role: 'user', content: input };
    setMessages((prev) => [...prev, userMessage]);
    setInput('');
    setIsLoading(true);

    try {
      const response = await fetch('/api/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ message: input }),
      });

      const data = await response.json();
      const assistantMessage = { role: 'assistant', content: data.content };

      setMessages((prev) => [...prev, assistantMessage]);
    } catch (error) {
      setMessages((prev) => [
        ...prev,
        { role: 'assistant', content: 'Something went wrong. Please try again.' },
      ]);
    } finally {
      setIsLoading(false);
    }
  }

  return (
    <main className="max-w-3xl mx-auto p-4">
      <div className="bg-gray-100 rounded p-4 h-[500px] overflow-y-auto mb-4">
        {messages.map((msg, i) => (
          <ChatMessage key={i} message={msg} />
        ))}
      </div>
      <ChatInput
        input={input}
        setInput={setInput}
        handleSubmit={handleSubmit}
        isLoading={isLoading}
      />
    </main>
  );
}
```

### Step 4: Simple Chat UI

In order to structure how the chatbot itself looks, we would need ChatInput.tsx and ChatMessage.tsx as components that help manage how the input looks to users when they type questions + display user queries in the chat-like format. 

components/ui/ChatInput.tsx:

```
import React from 'react';

interface ChatInputProps {
  input: string;
  setInput: (input: string) => void;
  handleSubmit: (e: React.FormEvent) => Promise<void>;
  isLoading: boolean;
}

export default function ChatInput({ input, setInput, handleSubmit, isLoading }: ChatInputProps) {
  return (
    <form onSubmit={handleSubmit} className="relative flex w-full">
      <input
        type="text"
        value={input}
        onChange={(e) => setInput(e.target.value)}
        placeholder="Ask me about customers, products, or orders..."
        className="w-full px-4 py-3 pr-16 rounded-xl border border-gray-200 focus:border-gray-500 focus:ring-2 focus:ring-gray-100 outline-none transition-all"
        disabled={isLoading}
      />
      <button
        type="submit"
        disabled={isLoading}
        className="absolute right-3 top-1/2 -translate-y-1/2 p-2 rounded-lg bg-gray-800 hover:bg-gray-900 text-white transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
      >
        {isLoading ? '...' : 'Send'}
      </button>
    </form>
  );
}
```



components/ui/ChatMessage.tsx: 

```
import React from 'react';
import { Message } from '@/app/types/chat';

interface ChatMessageProps {
  message: Message;
}

export default function ChatMessage({ message }: ChatMessageProps) {
  return (
    <div
      className={`flex ${
        message.role === 'user' ? 'justify-end' : 'justify-start'
      }`}
    >
      <div
        className={`max-w-[80%] rounded-sm px-4 py-3 font-light ${
          message.role === 'user'
            ? 'bg-black text-white'
            : 'bg-gray-50 border border-gray-200'
        }`}
      >
        <pre className="whitespace-pre-wrap font-mono text-sm">
          {message.content}
        </pre>
      </div>
    </div>
  );
}
```





### Security Note
For production:

- Move OpenAI Calls to API Routes:
- Protect API keys by handling all OpenAI calls server-side in /api/chat.
- Add Authentication:
- Use tools like NextAuth.js to restrict access, ensuring only authorized users can query the app.
- Set Up CORS: Allow requests only from trusted domains to secure your backend.
- Secure environment vairables.

### Recap & Overview

As you can see below, our app flow is as follows: 



![ecommerce-assistant-chatbot](https://hackmd.io/_uploads/BJBsf26L1l.png)

### Data Pipeline:

- Stripe API provides structured data (customers, products, invoices).
- Airbyte syncs this data into Supabase with PGVector enabled, allowing semantic search.

### Query Flow:
- User questions are sent from the frontend to a backend API.
- OpenAI converts the query into embeddings, and GPT categorizes it (e.g., customer, product, or order).
- Supabase retrieves relevant data using vector similarity, which GPT transforms into a meaningful response.

### Key Features:

- PGVector: Performs vector similarity searches on e-commerce data.
- Supabase SQL Functions: Route queries to the correct tables.
- OpenAI GPT: Enhances the experience with human-like responses.
- Next.js Frontend: Provides a user-friendly, real-time chat interface.


