# UI/UX Design System: 作業管理表 v3.0 (Commercial Grade)

## 1. Design Philosophy
- **Clean & Spacious**: Increase whitespace to reduce cognitive load.
- **Data-First**: The table is the hero. Minimize distractions.
- **Feedback-Rich**: Every action (hover, click, drag) provides immediate visual feedback.
- **Consistent**: Unified color palette and typography scale.

## 2. Design Tokens

### 2.1 Color Palette
We will move away from generic "Blue/Red" to a refined palette.

| Token | Tailwind Class | Hex (Approx) | Usage |
|:---|:---|:---|:---|
| **Primary** | `indigo-600` | `#4F46E5` | Main Actions, Active States, Links |
| **Primary Hover** | `indigo-700` | `#4338CA` | Hover on Primary |
| **Surface** | `white` | `#FFFFFF` | Cards, Table Rows |
| **Background** | `gray-50` | `#F9FAFB` | App Background |
| **Surface Alt** | `gray-50` | `#F9FAFB` | Table Header, Hover Rows |
| **Border** | `gray-200` | `#E5E7EB` | Dividers, Inputs |
| **Text Main** | `gray-900` | `#111827` | Headings, Primary Data |
| **Text Muted** | `gray-500` | `#6B7280` | Meta data, Help text |
| **Danger** | `rose-500` | `#F43F5E` | Delete, Overdue, Error |
| **Success** | `emerald-500` | `#10B981` | Completed, Success Toast |
| **Warning** | `amber-500` | `#F59E0B` | Warning Toast |

### 2.2 Typography
- **Font Family**: System Stack (`Inter`, `system-ui`, `-apple-system`).
- **Scale**:
    - **Page Title**: `text-2xl font-bold text-gray-900 tracking-tight`
    - **Section Header**: `text-lg font-semibold text-gray-800`
    - **Body**: `text-sm text-gray-900`
    - **Small**: `text-xs text-gray-500`

### 2.3 Spacing & Layout
- **Global Padding**: `p-6` or `p-8` for main container (was `p-4`).
- **Card Padding**: `p-6` (was `p-4` or `p-3`).
- **Gap**: `gap-4` or `gap-6` between major sections.
- **Table Density**:
    - Header: `px-6 py-3`
    - Cell: `px-6 py-4` (Compact: `px-4 py-2`)

### 2.4 Shadows & depth
- **Card**: `shadow-sm border border-gray-200` (Subtle)
- **Dropdown/Modal**: `shadow-xl ring-1 ring-black ring-opacity-5` (Elevated)

## 3. Component Specs

### 3.1 Data Table (The Core)
- **Container**: `bg-white rounded-xl shadow-sm border border-gray-200 overflow-hidden`
- **Header**:
    - Background: `bg-gray-50`
    - Text: `text-xs font-semibold text-gray-500 uppercase tracking-wider`
    - Sticky Top: `sticky top-0 z-10 border-b border-gray-200`
- **Rows**:
    - Hover: `hover:bg-gray-50 transition-colors duration-150`
    - Border: `border-b border-gray-100 last:border-0`
- **Status Badges**:
    - **Pill Shape**: `rounded-full px-2.5 py-0.5 text-xs font-medium`
    - **Dot**: Optional colored dot `w-1.5 h-1.5 rounded-full mr-1.5`

### 3.2 Filter Bar
- **Style**: Floating bar or integrated top bar.
- **Inputs**: `rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm`
- **Active State**: Highlighted background for active filters.

### 3.3 Buttons
- **Primary**: `inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md shadow-sm text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500`
- **Secondary**: `bg-white border-gray-300 text-gray-700 hover:bg-gray-50`
- **Icon Only**: `p-2 text-gray-400 hover:text-gray-500 hover:bg-gray-100 rounded-full`

### 3.4 Modals
- **Backdrop**: `bg-gray-500 bg-opacity-75 transition-opacity` (Blur optional)
- **Panel**: `bg-white rounded-lg shadow-xl transform transition-all sm:max-w-lg sm:w-full`
- **Input Fields**: Labeled with `block text-sm font-medium text-gray-700 mb-1`.

## 4. Micro-Interactions
- **Transitions**: `transition-all duration-200 ease-in-out` on all interactive elements.
- **Toasts**: Slide in from bottom-right or top-right. Dismissible.
- **Loading**: Pulse skeletons instead of pure spinners where possible.
