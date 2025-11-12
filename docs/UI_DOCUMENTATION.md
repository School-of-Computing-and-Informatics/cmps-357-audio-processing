# User Interface Documentation

## Web Interface Features

### Main Page Layout

The application features a modern, gradient-themed interface with a single-page application design:

#### 1. Header Section
- **Title**: "🎵 Audio Processing"
- **Subtitle**: "Upload and process your audio files with professional effects"
- **Design**: Clean typography with gradient purple background

#### 2. Upload Section
- **File Selector**: 
  - Styled button: "Choose Audio File"
  - Supported formats: MP3, AAC, AC3
  - File name display after selection
- **Upload Button**: 
  - Green "Upload & Analyze" button
  - Disabled until file is selected
  - Shows loading spinner during upload

#### 3. Statistics Section (appears after upload)
- **Title**: "📊 Audio Statistics"
- **Statistics Grid**: 6 cards displaying:
  1. **Max Level**: Peak dBFS value
  2. **Min Level**: Minimum dBFS value
  3. **Total Duration**: Length in seconds
  4. **Non-Silence**: Active audio duration
  5. **Sample Rate**: Frequency in Hz
  6. **Channels**: Mono or Stereo
- **Design**: Gradient purple cards with white text

#### 4. Processing Section (appears after upload)
- **Title**: "⚙️ Audio Processing"
- **Operation Selector**: Dropdown menu
  - Options: Compressor, Limiter
- **Dynamic Parameters**: Changes based on selected operation
  
  **Compressor Parameters**:
  - Threshold (dB): -60 to 0, default -20
  - Ratio: 1 to 20, default 4
  - Attack (ms): 0 to 100, default 5
  - Release (ms): 10 to 500, default 50
  
  **Limiter Parameters**:
  - Threshold (dB): -10 to 0, default -1
  - Release (ms): 10 to 500, default 50

- **Process Button**: Full-width gradient purple button
- **Loading Indicator**: Spinner during processing

#### 5. Download Section (appears after processing)
- **Success Message**: "✅ Processing Complete!"
- **Description**: "Your processed audio file is ready for download."
- **Download Button**: Green button with file download

### Color Scheme

- **Primary Gradient**: Purple (#667eea to #764ba2)
- **Background**: White with gradient overlay
- **Success**: Green (#28a745)
- **Error**: Red (#f8d7da)
- **Accent**: Light purple (#f8f9ff)

### Interactive Elements

1. **File Upload**:
   - Drag-and-drop styled upload area
   - Hover effects on buttons
   - Real-time file name display

2. **Statistics Display**:
   - Animated cards
   - Color-coded information
   - Clear value presentation

3. **Processing Controls**:
   - Responsive parameter inputs
   - Value validation
   - Real-time parameter updates
   - Helpful descriptions for each parameter

4. **Feedback**:
   - Loading spinners during operations
   - Error messages in red boxes
   - Success confirmations
   - Smooth transitions between sections

### Responsive Design

- **Desktop**: Full-width layout with grid system
- **Tablet**: Adjusted grid (2 columns for stats)
- **Mobile**: Single column layout
- **Max Width**: 900px centered container

### User Experience Flow

```
1. User arrives at homepage
   ↓
2. Selects audio file (mp3/aac/ac3)
   ↓
3. Clicks "Upload & Analyze"
   ↓ (loading spinner)
4. Views audio statistics in cards
   ↓
5. Selects processing operation (Compressor/Limiter)
   ↓
6. Adjusts parameters (optional)
   ↓
7. Clicks "Apply Processing"
   ↓ (loading spinner)
8. Sees success message
   ↓
9. Downloads processed file
```

### Accessibility Features

- Clear labels for all inputs
- Descriptive button text
- Visual feedback for all actions
- Error messages with context
- Loading indicators for async operations

### Browser Compatibility

- Modern browsers (Chrome, Firefox, Safari, Edge)
- ES6+ JavaScript features
- CSS Grid and Flexbox
- Fetch API for AJAX requests

## Screenshots Description

Since this is a text-based implementation, here's what users would see:

1. **Initial Load**: Beautiful gradient purple background with white centered card, file upload area with dashed border

2. **File Selected**: Upload button becomes active (green), file name appears below selector

3. **Statistics View**: Six purple gradient cards displaying audio metrics in a responsive grid

4. **Processing Controls**: Dropdown menu and parameter inputs with helpful descriptions in light purple background

5. **Success State**: Light blue download section with green download button

6. **Error State**: Red error message box at top of page with clear error description
