# PHASE_9_4_1_PLAN.md — UI Foundation & Scaffold (Next.js)

## 🎯 Objectives
1) Replace current React/Vite UI shell with **Next.js 14 + TypeScript + Tailwind + shadcn/ui** app
2) Implement API client with Zod envelope guards and React Query
3) Add global error boundary and proper error handling
4) Create `/overview` route with placeholder health cards
5) Maintain single-origin architecture from Phase 9.4.0

## 🏗 Architecture

### **Technology Stack**
- **Next.js 14** with App Router
- **TypeScript** for type safety
- **Tailwind CSS** for styling
- **shadcn/ui** for component library
- **React Query (TanStack Query)** for data fetching
- **Zod** for runtime validation
- **MSW** for API mocking in development

### **Project Structure**
```
ui/
├── app/                    # Next.js App Router
│   ├── (dashboard)/        # Grouped routes
│   │   ├── layout.tsx      # Dashboard layout
│   │   ├── overview/       # Overview page
│   │   │   └── page.tsx    # Health cards
│   │   └── globals.css     # Global styles
│   ├── api/                # API routes (if needed)
│   └── page.tsx            # Root page
├── components/             # Reusable components
│   ├── ui/                 # shadcn/ui components
│   └── dashboard/          # Dashboard-specific components
├── lib/                    # Utility libraries
│   ├── api.ts              # API client with envelope validation
│   ├── schemas.ts          # Zod schemas for API responses
│   ├── query.ts            # React Query configuration
│   └── state.ts            # Global state management
├── types/                  # TypeScript type definitions
└── package.json            # Dependencies and scripts
```

## 🔩 Implementation Steps

### **1. Initialize Next.js Project**
- Create new Next.js 14 project with TypeScript
- Configure Tailwind CSS
- Set up shadcn/ui component library
- Configure proper TypeScript settings

### **2. API Client Implementation**
- Create `lib/api.ts` with fetch wrapper
- Implement Zod schema validation for envelope format
- Add error handling and retry logic
- Create typed API functions

### **3. React Query Setup**
- Configure React Query provider
- Create query hooks for API endpoints
- Implement proper caching and invalidation
- Add loading and error states

### **4. Global Error Boundary**
- Create error boundary component
- Implement error reporting and recovery
- Add user-friendly error messages

### **5. Dashboard Layout**
- Create responsive dashboard layout
- Add navigation and sidebar
- Implement proper routing structure

### **6. Overview Page**
- Create health cards component
- Display system status and metrics
- Add quick actions and navigation

### **7. Development Scripts**
- Create `scripts/ui_dev.sh` for development
- Create `scripts/ui_build.sh` for production builds
- Update Docker configuration for new UI

## 🧪 Testing Strategy

### **Unit Tests**
- API client validation
- React Query hooks
- Component rendering
- Error boundary functionality

### **Integration Tests**
- API integration with real endpoints
- Routing and navigation
- State management

### **E2E Tests**
- Basic user flows
- Error scenarios
- Responsive design

## ✅ Acceptance Criteria

1. **Next.js 14 Setup**: Project runs with `npm run dev`
2. **TypeScript**: All code properly typed
3. **Tailwind + shadcn/ui**: Styled components working
4. **API Client**: Validates envelope format `{status,data,error}`
5. **React Query**: Data fetching with caching
6. **Error Boundary**: Graceful error handling
7. **Overview Page**: Health cards displaying system status
8. **Routing**: `/overview` route accessible
9. **Development**: Hot reload working
10. **Build**: Production build successful

## 🔜 Integration with Phase 9.4.0

- **Maintain Proxy Routing**: Keep Caddy routing `/api/**` → FastAPI, `/*` → Next.js
- **Update Docker**: Modify UI service to use Next.js instead of Vite
- **Preserve API Contract**: No changes to existing API endpoints
- **Health Endpoint**: Continue using `/api/health/full` for system status

## 📋 Deliverables

### **Core Files**
- `ui/package.json` (Next.js dependencies)
- `ui/next.config.js` (Next.js configuration)
- `ui/tailwind.config.js` (Tailwind configuration)
- `ui/components.json` (shadcn/ui configuration)

### **Application Files**
- `ui/app/(dashboard)/layout.tsx`
- `ui/app/(dashboard)/overview/page.tsx`
- `ui/app/page.tsx` (root redirect)

### **Library Files**
- `ui/lib/api.ts` (API client)
- `ui/lib/schemas.ts` (Zod schemas)
- `ui/lib/query.ts` (React Query setup)
- `ui/lib/state.ts` (Global state)

### **Components**
- `ui/components/ui/` (shadcn/ui components)
- `ui/components/dashboard/HealthCards.tsx`
- `ui/components/dashboard/ErrorBoundary.tsx`

### **Scripts**
- `scripts/ui_dev.sh`
- `scripts/ui_build.sh`

### **Configuration**
- `ui/tsconfig.json`
- `ui/.eslintrc.json`
- `ui/.prettierrc`

## 🚀 Migration Strategy

1. **Parallel Development**: Build new UI alongside existing Vite shell
2. **Feature Parity**: Ensure all current functionality works
3. **Gradual Migration**: Replace Vite shell with Next.js
4. **Testing**: Comprehensive testing before switchover
5. **Rollback Plan**: Ability to revert to Vite shell if needed

## 🎯 Success Metrics

- **Performance**: Faster initial load and better caching
- **Developer Experience**: Better TypeScript support and hot reload
- **User Experience**: Improved error handling and loading states
- **Maintainability**: Better component organization and reusability
- **Scalability**: Foundation for future UI features
