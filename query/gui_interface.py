"""
GUI interface for the multimodal RAG system using tkinter.
"""

import tkinter as tk
from tkinter import ttk, scrolledtext, filedialog, messagebox
import threading
import logging
from typing import List, Dict, Any

logger = logging.getLogger(__name__)

class GUIInterface:
    """Graphical user interface for the RAG system."""
    
    def __init__(self):
        """Initialize GUI interface."""
        self.root = tk.Tk()
        self.root.title("Multimodal RAG System")
        self.root.geometry("800x600")
        
        # Initialize components
        self.query_history = []
        self.setup_ui()
    
    def setup_ui(self):
        """Set up the user interface."""
        # Create main frame
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(2, weight=1)
        
        # Query input
        ttk.Label(main_frame, text="Question:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.query_entry = ttk.Entry(main_frame, width=50)
        self.query_entry.grid(row=0, column=1, sticky=(tk.W, tk.E), pady=5, padx=(5, 0))
        self.query_entry.bind("<Return>", self.on_query)
        
        # Query button
        query_button = ttk.Button(main_frame, text="Ask", command=self.on_query)
        query_button.grid(row=0, column=2, pady=5, padx=(5, 0))
        
        # Mode selection
        ttk.Label(main_frame, text="Mode:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.mode_var = tk.StringVar(value="text")
        mode_frame = ttk.Frame(main_frame)
        mode_frame.grid(row=1, column=1, sticky=tk.W, pady=5)
        
        ttk.Radiobutton(mode_frame, text="Text", variable=self.mode_var, value="text").pack(side=tk.LEFT)
        ttk.Radiobutton(mode_frame, text="Image", variable=self.mode_var, value="image").pack(side=tk.LEFT, padx=(10, 0))
        ttk.Radiobutton(mode_frame, text="Hybrid", variable=self.mode_var, value="hybrid").pack(side=tk.LEFT, padx=(10, 0))
        
        # Results area
        ttk.Label(main_frame, text="Results:").grid(row=2, column=0, sticky=(tk.W, tk.N), pady=(10, 5))
        
        # Create notebook for results tabs
        self.notebook = ttk.Notebook(main_frame)
        self.notebook.grid(row=2, column=1, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(10, 0))
        
        # Answer tab
        self.answer_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.answer_frame, text="Answer")
        self.answer_text = scrolledtext.ScrolledText(self.answer_frame, wrap=tk.WORD, width=70, height=20)
        self.answer_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Sources tab
        self.sources_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.sources_frame, text="Sources")
        self.sources_text = scrolledtext.ScrolledText(self.sources_frame, wrap=tk.WORD, width=70, height=20)
        self.sources_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Status bar
        self.status_var = tk.StringVar(value="Ready")
        status_bar = ttk.Label(main_frame, textvariable=self.status_var, relief=tk.SUNKEN, anchor=tk.W)
        status_bar.grid(row=3, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(10, 0))
    
    def on_query(self, event=None):
        """Handle query submission."""
        query = self.query_entry.get().strip()
        if not query:
            return
        
        # Add to history
        self.query_history.append(query)
        
        # Update UI
        self.status_var.set("Processing query...")
        self.answer_text.delete(1.0, tk.END)
        self.sources_text.delete(1.0, tk.END)
        
        # Disable UI during processing
        self.query_entry.config(state=tk.DISABLED)
        for child in self.root.winfo_children():
            for grandchild in child.winfo_children():
                if isinstance(grandchild, ttk.Button):
                    grandchild.config(state=tk.DISABLED)
        
        # Process in separate thread to avoid blocking UI
        thread = threading.Thread(target=self.process_query, args=(query,))
        thread.daemon = True
        thread.start()
    
    def process_query(self, query: str):
        """Process the query in a separate thread."""
        try:
            # Import here to avoid circular imports
            from retrieval.retriever import Retriever
            from generation.generator import Generator
            from indexing.vector_store import VectorStore
            from embedding.text_embedder import TextEmbedder
            from embedding.image_embedder import ImageEmbedder
            from utils.config import config
            
            # Initialize components
            vector_store = VectorStore(
                dimension=config.get('models.text_embedding.dim', 384),
                index_path=config.get('vector_db.index_path'),
                metadata_path=config.get('vector_db.metadata_path')
            )
            
            text_embedder = TextEmbedder(config.get('models.text_embedding.name'))
            image_embedder = ImageEmbedder(config.get('models.image_embedding.name'))
            retriever = Retriever(vector_store, text_embedder, image_embedder)
            generator = Generator(
                model_name=config.get('models.llm.name'),
                max_tokens=config.get('models.llm.max_tokens', 2048)
            )
            
            # Retrieve context
            mode = self.mode_var.get()
            if mode == 'image':
                # For image mode, we'd need an image path - not implemented in this GUI version
                context = []
            else:
                context = retriever.retrieve_text(query, k=config.get('retrieval.top_k', 5))
            
            # Generate answer
            if context:
                answer = generator.generate_answer(query, context)
                sources = self.format_sources(context)
            else:
                answer = "No relevant context found for your query."
                sources = "No sources available."
            
            # Update UI in main thread
            self.root.after(0, self.update_results, answer, sources)
        except Exception as e:
            logger.error(f"Error processing query: {str(e)}")
            self.root.after(0, self.show_error, str(e))
    
    def update_results(self, answer: str, sources: str):
        """Update the results in the UI."""
        self.answer_text.delete(1.0, tk.END)
        self.answer_text.insert(tk.END, answer)
        
        self.sources_text.delete(1.0, tk.END)
        self.sources_text.insert(tk.END, sources)
        
        self.status_var.set("Ready")
        self.query_entry.config(state=tk.NORMAL)
        
        # Re-enable UI
        for child in self.root.winfo_children():
            for grandchild in child.winfo_children():
                if isinstance(grandchild, ttk.Button):
                    grandchild.config(state=tk.NORMAL)
    
    def show_error(self, error: str):
        """Show error message."""
        self.status_var.set("Error occurred")
        messagebox.showerror("Error", f"An error occurred: {error}")
        
        self.query_entry.config(state=tk.NORMAL)
        for child in self.root.winfo_children():
            for grandchild in child.winfo_children():
                if isinstance(grandchild, ttk.Button):
                    grandchild.config(state=tk.NORMAL)
    
    def format_sources(self, context: List[Dict[str, Any]]) -> str:
        """
        Format sources for display.
        
        Args:
            context: Retrieved context items
            
        Returns:
            Formatted sources string
        """
        sources = []
        for i, item in enumerate(context, 1):
            source = item.get('source', 'Unknown')
            item_type = item.get('type', 'unknown')
            
            if item_type == 'text':
                page = item.get('page', '')
                paragraph = item.get('paragraph', '')
                text = item.get('text', '')[:100] + "..." if len(item.get('text', '')) > 100 else item.get('text', '')
                
                source_info = f"[{i}] {source}"
                if page or paragraph:
                    details = []
                    if page:
                        details.append(f"Page {page}")
                    if paragraph:
                        details.append(f"Paragraph {paragraph}")
                    source_info += f" ({', '.join(details)})"
                source_info += f"\n{text}\n"
                sources.append(source_info)
            elif item_type == 'image':
                sources.append(f"[{i}] Image: {source}\n")
            elif item_type == 'audio':
                sources.append(f"[{i}] Audio: {source}\n")
        
        return "\n".join(sources)
    
    def run(self):
        """Run the GUI application."""
        self.root.mainloop()