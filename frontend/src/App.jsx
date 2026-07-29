import { useState, useEffect, useRef } from 'react';
import ReactMarkdown from 'react-markdown';
import './index.css';

function App() {
  const [request, setRequest] = useState('');
  const [loading, setLoading] = useState(false);
  const [itinerary, setItinerary] = useState(null);
  const [error, setError] = useState(null);

  // Voice States
  const [isListening, setIsListening] = useState(false);
  const [isSpeaking, setIsSpeaking] = useState(false);
  const recognitionRef = useRef(null);

  // Initialize Speech Recognition
  useEffect(() => {
    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
    if (SpeechRecognition) {
      const recognition = new SpeechRecognition();
      recognition.continuous = true;
      recognition.interimResults = true;
      
      recognition.onresult = (event) => {
        let currentTranscript = '';
        for (let i = event.resultIndex; i < event.results.length; i++) {
          if (event.results[i].isFinal) {
            currentTranscript += event.results[i][0].transcript + ' ';
          }
        }
        if (currentTranscript) {
          setRequest((prev) => prev + currentTranscript);
        }
      };

      recognition.onerror = (event) => {
        console.error('Speech recognition error', event.error);
        setIsListening(false);
      };

      recognition.onend = () => {
        setIsListening(false);
      };

      recognitionRef.current = recognition;
    }
  }, []);

  const toggleListening = () => {
    if (isListening) {
      recognitionRef.current?.stop();
      setIsListening(false);
    } else {
      if (!recognitionRef.current) {
        alert("Speech Recognition is not supported in this browser.");
        return;
      }
      recognitionRef.current.start();
      setIsListening(true);
    }
  };

  const toggleSpeaking = () => {
    if (isSpeaking) {
      window.speechSynthesis.cancel();
      setIsSpeaking(false);
    } else if (itinerary) {
      const cleanText = itinerary.replace(/[#*_~`\[\]]/g, '');
      const utterance = new SpeechSynthesisUtterance(cleanText);
      utterance.onend = () => setIsSpeaking(false);
      window.speechSynthesis.speak(utterance);
      setIsSpeaking(true);
    }
  };

  const handleGenerate = async () => {
    if (!request.trim()) return;
    
    if (isListening) toggleListening();
    if (isSpeaking) toggleSpeaking();
    
    setLoading(true);
    setError(null);
    setItinerary(null);
    
    try {
      const apiUrl = import.meta.env.VITE_API_URL || 'http://localhost:8000';
      const response = await fetch(`${apiUrl}/plan`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ request })
      });
      
      const data = await response.json();
      
      if (!data.success) {
        setError(data.feedback.join('\n'));
      } else {
        setItinerary(data.itinerary);
      }
    } catch (err) {
      setError('Failed to connect to the server. Please ensure the backend API is running on localhost:8000.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="text-on-surface font-body-md bg-background antialiased selection:bg-primary selection:text-on-primary overflow-x-hidden flex flex-col min-h-screen">
      {/* Top Navigation */}
      <header className="fixed top-0 w-full z-50 bg-surface/60 backdrop-blur-xl border-b border-white/10 shadow-sm">
        <div className="flex justify-between items-center h-16 px-gutter max-w-container-max mx-auto">
          <div className="text-headline-md font-headline-md font-bold text-transparent bg-clip-text bg-gradient-to-r from-[#ec4899] to-[#a855f7]">Tours Thambi</div>
          <nav className="hidden md:flex space-x-6">
            <a className="text-primary border-b-2 border-primary pb-1 font-body-md hover:scale-105 transition-transform duration-200 cursor-pointer active:scale-95" href="#">Discover</a>
            <a className="text-on-surface-variant hover:text-on-surface font-body-md hover:scale-105 transition-transform duration-200 cursor-pointer active:scale-95" href="#">My Trips</a>
            <a className="text-on-surface-variant hover:text-on-surface font-body-md hover:scale-105 transition-transform duration-200 cursor-pointer active:scale-95" href="#">Saved</a>
            <a className="text-on-surface-variant hover:text-on-surface font-body-md hover:scale-105 transition-transform duration-200 cursor-pointer active:scale-95" href="#">Support</a>
          </nav>
          <div className="flex items-center space-x-4">
            <button aria-label="Settings" className="text-on-surface-variant hover:text-on-surface transition-colors cursor-pointer active:scale-95">
              <span className="material-symbols-outlined">settings</span>
            </button>
            <button aria-label="Account" className="text-on-surface-variant hover:text-on-surface transition-colors cursor-pointer active:scale-95">
              <span className="material-symbols-outlined">account_circle</span>
            </button>
            <button className="hidden md:block bg-gradient-to-r from-[#ec4899] to-[#a855f7] text-white px-4 py-2 rounded-lg font-label-sm text-label-sm hover:scale-105 transition-transform duration-200 glow-effect cursor-pointer active:scale-95">
              Sign In
            </button>
          </div>
        </div>
      </header>
      
      <main className="flex-grow pt-32 pb-24 px-margin-mobile md:px-margin-desktop flex flex-col items-center justify-start relative z-10 w-full max-w-4xl mx-auto">
        {/* Hero Section */}
        <div className="text-center mb-12 max-w-2xl">
          <h1 className="font-display-lg-mobile md:font-display-lg text-display-lg-mobile md:text-display-lg text-transparent bg-clip-text bg-gradient-to-r from-[#ec4899] to-[#a855f7] mb-4">Agentic Trip Planner</h1>
          <p className="font-body-lg text-body-lg text-tertiary-container">
            Describe your dream trip to Japan, and our AI agents will coordinate to build the perfect, verified itinerary.
          </p>
        </div>

        {/* Input Card */}
        <div className="w-full glass-card rounded-xl p-6 mb-8 transition-all duration-300 relative group">
          <div className="absolute inset-0 bg-gradient-to-r from-[#ec4899] to-[#a855f7] opacity-0 group-hover:opacity-5 transition-opacity duration-500 rounded-xl pointer-events-none"></div>
          
          <div className="relative w-full mb-4">
            <textarea 
              className="w-full bg-[#020617]/50 border border-slate-700/50 rounded-lg p-4 min-h-[120px] text-on-surface font-body-md focus:border-[#a855f7] focus:ring-1 focus:ring-[#a855f7] transition-all resize-none placeholder-slate-500" 
              placeholder="I want to visit Tokyo for 5 days with a $2000 budget"
              value={request}
              onChange={(e) => setRequest(e.target.value)}
            ></textarea>
            <button 
              className={`absolute bottom-4 right-4 p-2 bg-surface-container rounded-full text-secondary hover:text-primary transition-colors hover:scale-110 active:scale-95 ${isListening ? 'listening' : ''} mic-btn`} 
              onClick={toggleListening}
              title={isListening ? "Stop listening" : "Start dictating"}
            >
              <span className="material-symbols-outlined" style={{ fontVariationSettings: "'FILL' 1" }}>
                {isListening ? 'mic_off' : 'mic'}
              </span>
            </button>
          </div>
          
          <button 
            className="w-full bg-gradient-to-r from-[#ec4899] to-[#a855f7] text-white rounded-lg py-3 flex items-center justify-center gap-2 font-subtitle-md text-subtitle-md font-semibold hover:scale-[1.02] transition-transform duration-200 glow-effect cursor-pointer active:scale-95 shadow-lg"
            onClick={handleGenerate}
            disabled={loading}
          >
            {loading ? (
              <><span className="material-symbols-outlined animate-spin" style={{ fontVariationSettings: "'FILL' 1" }}>sync</span> Agents Coordinating...</>
            ) : (
              <><span className="material-symbols-outlined" style={{ fontVariationSettings: "'FILL' 1" }}>auto_awesome</span> Generate Itinerary</>
            )}
          </button>
        </div>

        {/* Error Card */}
        {error && (
          <div className="w-full glass-card rounded-xl p-6 mb-8 transition-all duration-300 relative group" style={{ borderColor: 'rgba(220, 38, 38, 0.5)' }}>
            <h2 className="font-headline-md text-headline-md flex items-center gap-3 text-error mb-4">
              <span className="material-symbols-outlined" style={{ fontVariationSettings: "'FILL' 1" }}>error</span>
              Planning Failed
            </h2>
            <p className="font-body-md text-body-md text-on-surface-variant whitespace-pre-wrap">{error}</p>
          </div>
        )}

        {/* Output Card */}
        {itinerary && (
          <div className="w-full glass-card rounded-xl p-6 transition-all duration-300 relative group" id="output-card">
            {/* Simulated Pulse Indicator */}
            <div className="absolute top-0 left-0 w-full h-1 bg-gradient-to-r from-transparent via-[#a855f7] to-transparent opacity-50 animate-pulse rounded-t-xl"></div>
            
            <div className="flex justify-between items-center mb-6 border-b border-white/10 pb-4">
              <h2 className="font-headline-md text-headline-md flex items-center gap-3 text-secondary">
                <span className="material-symbols-outlined" style={{ fontVariationSettings: "'FILL' 1" }}>map</span>
                Your Custom Itinerary
              </h2>
              <button 
                className={`p-2 bg-surface-container/50 rounded-full text-tertiary hover:text-white transition-colors hover:scale-110 active:scale-95 border border-white/5 ${isSpeaking ? 'speaking' : ''} tts-btn`}
                onClick={toggleSpeaking} 
                title={isSpeaking ? "Stop reading" : "Read aloud"}
              >
                <span className="material-symbols-outlined" style={{ fontVariationSettings: "'FILL' 1" }}>
                  {isSpeaking ? 'volume_off' : 'volume_up'}
                </span>
              </button>
            </div>
            
            <div className="space-y-4 font-body-md text-body-md text-on-surface-variant">
              <ReactMarkdown 
                components={{
                  h3: ({node, ...props}) => <div className="p-4 bg-surface-container-low/50 rounded-lg border border-white/5 hover:bg-surface-container/80 transition-colors"><h3 className="text-on-surface font-semibold mb-2 flex items-center gap-2" {...props} /></div>,
                  ul: ({node, ...props}) => <ul className="list-disc list-inside space-y-1 ml-2 text-sm" {...props} />,
                  li: ({node, ...props}) => <li className="" {...props} />
                }}
              >
                {itinerary}
              </ReactMarkdown>
            </div>
          </div>
        )}
      </main>

      {/* Footer */}
      <footer className="w-full py-12 bg-surface-container-lowest border-t border-white/5 mt-auto">
        <div className="flex flex-col md:flex-row justify-between items-center px-gutter max-w-container-max mx-auto gap-4">
          <div className="font-headline-md text-headline-md text-on-surface text-sm opacity-50">Agentic Trip Planner</div>
          <div className="flex space-x-6 font-label-sm text-label-sm">
            <a className="text-on-surface-variant hover:text-primary transition-colors" href="#">Privacy Policy</a>
            <a className="text-on-surface-variant hover:text-primary transition-colors" href="#">Terms of Service</a>
            <a className="text-on-surface-variant hover:text-primary transition-colors" href="#">Contact Us</a>
          </div>
          <div className="text-secondary font-label-sm text-label-sm text-xs opacity-70">© 2024 Agentic Trip Planner. Powered by Deep Space AI.</div>
        </div>
      </footer>
    </div>
  );
}

export default App;
