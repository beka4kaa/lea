"""Magic UI provider implementation with enhanced code templates."""

import json
import re
from typing import List, Optional, Dict, Any
from datetime import datetime

from .base import GitHubProvider, ComponentNotFoundError
from .registry import register_provider
from ..models.component_manifest import (
    ComponentManifest,
    Provider,
    License,
    LicenseType,
    Source,
    Framework,
    TailwindConfig,
    TailwindVersion,
    ComponentCode,
    ComponentAccess,
    InstallPlan,
    ComponentCategory
)

# Enhanced code templates for Magic UI components
MAGICUI_CODE_TEMPLATES = {
    "magic-button": {
        "tsx": '''import React from "react";
import { motion } from "framer-motion";
import { cn } from "@/lib/utils";

interface MagicButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  children: React.ReactNode;
  className?: string;
}

export default function MagicButton({
  children,
  className,
  ...props
}: MagicButtonProps) {
  return (
    <motion.button
      className={cn(
        "relative inline-flex h-12 overflow-hidden rounded-full p-[1px] focus:outline-none focus:ring-2 focus:ring-slate-400 focus:ring-offset-2 focus:ring-offset-slate-50",
        className
      )}
      whileHover={{ scale: 1.05 }}
      whileTap={{ scale: 0.95 }}
      {...props}
    >
      <span className="absolute inset-[-1000%] animate-[spin_2s_linear_infinite] bg-[conic-gradient(from_90deg_at_50%_50%,#E2CBFF_0%,#393BB2_50%,#E2CBFF_100%)]" />
      <span className="inline-flex h-full w-full cursor-pointer items-center justify-center rounded-full bg-slate-950 px-3 py-1 text-sm font-medium text-white backdrop-blur-3xl">
        {children}
      </span>
    </motion.button>
  );
}''',
        "dependencies": ["framer-motion", "clsx", "tailwind-merge"],
        "description": "A magical button with animated gradient border and hover effects."
    },
    
    "rainbow-button": {
        "tsx": '''import React from "react";
import { motion } from "framer-motion";
import { cn } from "@/lib/utils";

interface RainbowButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  children: React.ReactNode;
  className?: string;
}

export default function RainbowButton({
  children,
  className,
  ...props
}: RainbowButtonProps) {
  return (
    <motion.button
      className={cn(
        "group relative inline-flex h-11 items-center justify-center overflow-hidden rounded-md bg-neutral-950 px-6 font-medium text-neutral-200 transition hover:scale-110",
        className
      )}
      whileHover={{ scale: 1.05 }}
      whileTap={{ scale: 0.95 }}
      {...props}
    >
      <span className="absolute inset-0 overflow-hidden rounded-md">
        <span className="absolute inset-0 rounded-md bg-gradient-to-r from-red-500 via-purple-500 to-blue-500 opacity-0 transition-opacity duration-500 group-hover:opacity-100" />
      </span>
      <span className="relative z-10">{children}</span>
    </motion.button>
  );
}''',
        "dependencies": ["framer-motion", "clsx", "tailwind-merge"],
        "description": "A button with rainbow gradient hover effect and smooth animations."
    },
    
    "marquee": {
        "tsx": '''import { cn } from "@/lib/utils";

interface MarqueeProps {
  className?: string;
  reverse?: boolean;
  pauseOnHover?: boolean;
  children?: React.ReactNode;
  vertical?: boolean;
  repeat?: number;
}

export default function Marquee({
  className,
  reverse,
  pauseOnHover = false,
  children,
  vertical = false,
  repeat = 4,
  ...props
}: MarqueeProps) {
  return (
    <div
      {...props}
      className={cn(
        "group flex overflow-hidden p-2 [--duration:20s] [--gap:1rem] [gap:var(--gap)]",
        {
          "flex-row": !vertical,
          "flex-col": vertical,
        },
        className,
      )}
    >
      {Array(repeat)
        .fill(0)
        .map((_, i) => (
          <div
            key={i}
            className={cn("flex shrink-0 justify-around [gap:var(--gap)]", {
              "animate-marquee flex-row": !vertical,
              "animate-marquee-vertical flex-col": vertical,
              "group-hover:[animation-play-state:paused]": pauseOnHover,
              "[animation-direction:reverse]": reverse,
            })}
          >
            {children}
          </div>
        ))}
    </div>
  );
}''',
        "dependencies": ["clsx", "tailwind-merge"],
        "description": "A marquee component for scrolling content horizontally or vertically."
    },
    
    "sparkles": {
        "tsx": '''import React from "react";
import { motion } from "framer-motion";
import { cn } from "@/lib/utils";

interface SparklesProps {
  children: React.ReactNode;
  className?: string;
  color?: string;
  size?: number;
}

export default function Sparkles({
  children,
  className,
  color = "rgba(255, 255, 255, 0.8)",
  size = 16,
}: SparklesProps) {
  const sparkles = Array.from({ length: 3 }, (_, i) => ({
    id: i,
    x: Math.random() * 100,
    y: Math.random() * 100,
    scale: Math.random() * 0.5 + 0.5,
  }));

  return (
    <span className={cn("relative inline-block", className)}>
      {sparkles.map((sparkle) => (
        <motion.div
          key={sparkle.id}
          className="pointer-events-none absolute"
          style={{
            left: `${sparkle.x}%`,
            top: `${sparkle.y}%`,
            transform: "translate(-50%, -50%)",
          }}
          animate={{
            scale: [0, sparkle.scale, 0],
            rotate: [0, 360],
            opacity: [0, 1, 0],
          }}
          transition={{
            duration: 2,
            repeat: Infinity,
            delay: sparkle.id * 0.5,
          }}
        >
          <div
            style={{
              width: size,
              height: size,
              backgroundColor: color,
            }}
            className="rounded-full"
          />
        </motion.div>
      ))}
      {children}
    </span>
  );
}''',
        "dependencies": ["framer-motion", "clsx", "tailwind-merge"],
        "description": "Add magical sparkle effects to any component."
    },
    
    "contact-form": {
        "tsx": '''import React, { useState } from "react";
import { motion } from "framer-motion";
import { cn } from "@/lib/utils";

interface ContactFormProps {
  className?: string;
  onSubmit?: (data: FormData) => void;
}

interface FormData {
  name: string;
  email: string;
  message: string;
}

export default function ContactForm({ className, onSubmit }: ContactFormProps) {
  const [formData, setFormData] = useState<FormData>({
    name: "",
    email: "",
    message: ""
  });
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [isSubmitted, setIsSubmitted] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsSubmitting(true);
    
    try {
      await new Promise(resolve => setTimeout(resolve, 1000));
      onSubmit?.(formData);
      setIsSubmitted(true);
      setFormData({ name: "", email: "", message: "" });
    } finally {
      setIsSubmitting(false);
    }
  };

  if (isSubmitted) {
    return (
      <motion.div
        initial={{ scale: 0.8, opacity: 0 }}
        animate={{ scale: 1, opacity: 1 }}
        className={cn("p-8 text-center bg-green-50 rounded-lg border border-green-200", className)}
      >
        <div className="text-green-600 text-2xl mb-2">✓</div>
        <h3 className="text-green-800 font-semibold mb-2">Message Sent!</h3>
        <p className="text-green-700">Thank you for your message. We'll get back to you soon.</p>
        <button
          onClick={() => setIsSubmitted(false)}
          className="mt-4 text-green-600 hover:text-green-800 underline"
        >
          Send another message
        </button>
      </motion.div>
    );
  }

  return (
    <motion.form
      initial={{ y: 20, opacity: 0 }}
      animate={{ y: 0, opacity: 1 }}
      onSubmit={handleSubmit}
      className={cn("space-y-4 p-6 bg-white rounded-lg shadow-lg border", className)}
    >
      <div>
        <label htmlFor="name" className="block text-sm font-medium text-gray-700 mb-1">
          Name
        </label>
        <input
          type="text"
          id="name"
          required
          value={formData.name}
          onChange={(e) => setFormData(prev => ({ ...prev, name: e.target.value }))}
          className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
          placeholder="Your name"
        />
      </div>
      
      <div>
        <label htmlFor="email" className="block text-sm font-medium text-gray-700 mb-1">
          Email
        </label>
        <input
          type="email"
          id="email"
          required
          value={formData.email}
          onChange={(e) => setFormData(prev => ({ ...prev, email: e.target.value }))}
          className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
          placeholder="your@email.com"
        />
      </div>
      
      <div>
        <label htmlFor="message" className="block text-sm font-medium text-gray-700 mb-1">
          Message
        </label>
        <textarea
          id="message"
          required
          rows={4}
          value={formData.message}
          onChange={(e) => setFormData(prev => ({ ...prev, message: e.target.value }))}
          className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent resize-none"
          placeholder="Your message..."
        />
      </div>
      
      <motion.button
        type="submit"
        disabled={isSubmitting}
        whileHover={{ scale: 1.02 }}
        whileTap={{ scale: 0.98 }}
        className="w-full py-2 px-4 bg-blue-600 text-white rounded-md hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 disabled:bg-blue-400 disabled:cursor-not-allowed transition-colors"
      >
        {isSubmitting ? "Sending..." : "Send Message"}
      </motion.button>
    </motion.form>
  );
}''',
        "dependencies": ["framer-motion", "clsx", "tailwind-merge"],
        "description": "A complete contact form with validation, loading states, and success feedback."
    },
    
    "modal-dialog": {
        "tsx": '''import React, { useEffect } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { cn } from "@/lib/utils";

interface ModalProps {
  isOpen: boolean;
  onClose: () => void;
  title: string;
  children: React.ReactNode;
  className?: string;
  size?: "sm" | "md" | "lg" | "xl";
}

export default function Modal({ isOpen, onClose, title, children, className, size = "md" }: ModalProps) {
  useEffect(() => {
    const handleEscape = (e: KeyboardEvent) => {
      if (e.key === "Escape") onClose();
    };
    
    if (isOpen) {
      document.addEventListener("keydown", handleEscape);
      document.body.style.overflow = "hidden";
    }
    
    return () => {
      document.removeEventListener("keydown", handleEscape);
      document.body.style.overflow = "auto";
    };
  }, [isOpen, onClose]);

  const sizeClasses = {
    sm: "max-w-md",
    md: "max-w-lg",
    lg: "max-w-2xl",
    xl: "max-w-4xl"
  };

  return (
    <AnimatePresence>
      {isOpen && (
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          exit={{ opacity: 0 }}
          className="fixed inset-0 z-50 flex items-center justify-center p-4"
        >
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            onClick={onClose}
            className="absolute inset-0 bg-black bg-opacity-50"
          />
          
          <motion.div
            initial={{ scale: 0.9, opacity: 0, y: 20 }}
            animate={{ scale: 1, opacity: 1, y: 0 }}
            exit={{ scale: 0.9, opacity: 0, y: 20 }}
            className={cn(
              "relative w-full bg-white rounded-lg shadow-xl",
              sizeClasses[size],
              className
            )}
          >
            <div className="flex items-center justify-between p-6 border-b border-gray-200">
              <h2 className="text-xl font-semibold text-gray-900">{title}</h2>
              <button
                onClick={onClose}
                className="text-gray-400 hover:text-gray-600 focus:outline-none focus:text-gray-600 transition-colors"
              >
                <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                </svg>
              </button>
            </div>
            
            <div className="p-6">
              {children}
            </div>
          </motion.div>
        </motion.div>
      )}
    </AnimatePresence>
  );
}''',
        "dependencies": ["framer-motion", "clsx", "tailwind-merge"],
        "description": "A flexible modal dialog component with animations and keyboard support."
    },
    
    "loading-spinner": {
        "tsx": '''import React from "react";
import { motion } from "framer-motion";
import { cn } from "@/lib/utils";

interface LoadingSpinnerProps {
  className?: string;
  size?: "sm" | "md" | "lg";
  variant?: "spin" | "pulse" | "dots" | "bars";
  color?: string;
}

export default function LoadingSpinner({ 
  className, 
  size = "md", 
  variant = "spin",
  color = "currentColor"
}: LoadingSpinnerProps) {
  const sizeClasses = {
    sm: "w-4 h-4",
    md: "w-8 h-8",
    lg: "w-12 h-12"
  };

  if (variant === "spin") {
    return (
      <motion.div
        animate={{ rotate: 360 }}
        transition={{ duration: 1, repeat: Infinity, ease: "linear" }}
        className={cn(sizeClasses[size], className)}
      >
        <svg className="w-full h-full" fill="none" viewBox="0 0 24 24">
          <circle
            className="opacity-25"
            cx="12" cy="12" r="10"
            stroke={color} strokeWidth="4"
          />
          <path
            className="opacity-75"
            fill={color}
            d="m4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"
          />
        </svg>
      </motion.div>
    );
  }

  if (variant === "dots") {
    return (
      <div className={cn("flex space-x-1", className)}>
        {[0, 1, 2].map((i) => (
          <motion.div
            key={i}
            animate={{ y: [0, -8, 0], opacity: [0.5, 1, 0.5] }}
            transition={{ duration: 0.6, repeat: Infinity, delay: i * 0.2 }}
            className={cn(
              "rounded-full bg-current",
              size === "sm" ? "w-2 h-2" : size === "md" ? "w-3 h-3" : "w-4 h-4"
            )}
            style={{ color }}
          />
        ))}
      </div>
    );
  }

  return (
    <motion.div
      animate={{ scale: [1, 1.2, 1], opacity: [0.5, 1, 0.5] }}
      transition={{ duration: 1.5, repeat: Infinity }}
      className={cn("rounded-full bg-current", sizeClasses[size], className)}
      style={{ color }}
    />
  );
}''',
        "dependencies": ["framer-motion", "clsx", "tailwind-merge"],
        "description": "Animated loading spinner with multiple variants."
    },
    
    "tooltip": {
        "tsx": '''import React, { useState, useRef, useEffect } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { cn } from "@/lib/utils";

interface TooltipProps {
  children: React.ReactNode;
  content: React.ReactNode;
  position?: "top" | "bottom" | "left" | "right";
  className?: string;
  delay?: number;
}

export default function Tooltip({ 
  children, content, position = "top", className, delay = 500 
}: TooltipProps) {
  const [isVisible, setIsVisible] = useState(false);
  const triggerRef = useRef<HTMLDivElement>(null);
  const timeoutRef = useRef<NodeJS.Timeout>();

  const showTooltip = () => {
    if (timeoutRef.current) clearTimeout(timeoutRef.current);
    timeoutRef.current = setTimeout(() => setIsVisible(true), delay);
  };

  const hideTooltip = () => {
    if (timeoutRef.current) clearTimeout(timeoutRef.current);
    setIsVisible(false);
  };

  const positionClasses = {
    top: "bottom-full left-1/2 -translate-x-1/2 mb-2",
    bottom: "top-full left-1/2 -translate-x-1/2 mt-2",
    left: "right-full top-1/2 -translate-y-1/2 mr-2",
    right: "left-full top-1/2 -translate-y-1/2 ml-2"
  };

  const arrowClasses = {
    top: "top-full left-1/2 -translate-x-1/2 border-l-transparent border-r-transparent border-b-transparent border-t-gray-900",
    bottom: "bottom-full left-1/2 -translate-x-1/2 border-l-transparent border-r-transparent border-t-transparent border-b-gray-900",
    left: "left-full top-1/2 -translate-y-1/2 border-t-transparent border-b-transparent border-r-transparent border-l-gray-900",
    right: "right-full top-1/2 -translate-y-1/2 border-t-transparent border-b-transparent border-l-transparent border-r-gray-900"
  };

  return (
    <div
      ref={triggerRef}
      className="relative inline-block"
      onMouseEnter={showTooltip}
      onMouseLeave={hideTooltip}
      onFocus={showTooltip}
      onBlur={hideTooltip}
    >
      {children}
      
      <AnimatePresence>
        {isVisible && (
          <motion.div
            initial={{ opacity: 0, scale: 0.95 }}
            animate={{ opacity: 1, scale: 1 }}
            exit={{ opacity: 0, scale: 0.95 }}
            transition={{ duration: 0.15 }}
            className={cn(
              "absolute z-50 px-3 py-2 text-sm text-white bg-gray-900 rounded-md shadow-lg whitespace-nowrap",
              positionClasses[position],
              className
            )}
          >
            {content}
            <div className={cn("absolute w-0 h-0 border-4", arrowClasses[position])} />
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  );
}''',
        "dependencies": ["framer-motion", "clsx", "tailwind-merge"],
        "description": "Interactive tooltip component with positioning."
    },
    
    "image-gallery": {
        "tsx": '''import React, { useState } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { cn } from "@/lib/utils";

interface Image {
  id: string;
  src: string;
  alt: string;
  caption?: string;
}

interface ImageGalleryProps {
  images: Image[];
  className?: string;
  columns?: number;
}

export default function ImageGallery({ images, className, columns = 3 }: ImageGalleryProps) {
  const [selectedImage, setSelectedImage] = useState<Image | null>(null);

  return (
    <>
      <div 
        className={cn(
          "grid gap-4",
          {
            "grid-cols-1": columns === 1,
            "grid-cols-2": columns === 2,
            "grid-cols-3": columns === 3,
            "grid-cols-4": columns === 4,
          },
          className
        )}
      >
        {images.map((image, index) => (
          <motion.div
            key={image.id}
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: index * 0.1 }}
            className="cursor-pointer group relative overflow-hidden rounded-lg"
            onClick={() => setSelectedImage(image)}
          >
            <img
              src={image.src}
              alt={image.alt}
              className="w-full h-64 object-cover transition-transform duration-300 group-hover:scale-110"
            />
            <div className="absolute inset-0 bg-black bg-opacity-0 group-hover:bg-opacity-30 transition-all duration-300 flex items-center justify-center">
              <div className="text-white opacity-0 group-hover:opacity-100 transition-opacity duration-300">
                <svg className="w-8 h-8" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0zM10 7v3m0 0v3m0-3h3m-3 0H7" />
                </svg>
              </div>
            </div>
          </motion.div>
        ))}
      </div>

      <AnimatePresence>
        {selectedImage && (
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black bg-opacity-90"
            onClick={() => setSelectedImage(null)}
          >
            <motion.div
              initial={{ scale: 0.8, opacity: 0 }}
              animate={{ scale: 1, opacity: 1 }}
              exit={{ scale: 0.8, opacity: 0 }}
              className="relative max-w-4xl max-h-full"
              onClick={(e) => e.stopPropagation()}
            >
              <img
                src={selectedImage.src}
                alt={selectedImage.alt}
                className="max-w-full max-h-full object-contain"
              />
              {selectedImage.caption && (
                <p className="text-white text-center mt-4 text-lg">
                  {selectedImage.caption}
                </p>
              )}
              <button
                onClick={() => setSelectedImage(null)}
                className="absolute top-4 right-4 text-white hover:text-gray-300 transition-colors"
              >
                <svg className="w-8 h-8" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                </svg>
              </button>
            </motion.div>
          </motion.div>
        )}
      </AnimatePresence>
    </>
  );
}''',
        "dependencies": ["framer-motion", "clsx", "tailwind-merge"],
        "description": "Interactive image gallery with lightbox functionality."
    },
    
    "calculator": {
        "tsx": '''import React, { useState } from "react";
import { motion } from "framer-motion";
import { cn } from "@/lib/utils";

interface CalculatorProps {
  className?: string;
  onCalculate?: (result: number) => void;
}

export default function Calculator({ className, onCalculate }: CalculatorProps) {
  const [display, setDisplay] = useState("0");
  const [previousValue, setPreviousValue] = useState<number | null>(null);
  const [operation, setOperation] = useState<string | null>(null);
  const [waitingForOperand, setWaitingForOperand] = useState(false);

  const inputNumber = (num: string) => {
    if (waitingForOperand) {
      setDisplay(num);
      setWaitingForOperand(false);
    } else {
      setDisplay(display === "0" ? num : display + num);
    }
  };

  const inputOperation = (nextOperation: string) => {
    const inputValue = parseFloat(display);

    if (previousValue === null) {
      setPreviousValue(inputValue);
    } else if (operation) {
      const currentValue = previousValue || 0;
      const newValue = calculate(currentValue, inputValue, operation);
      setDisplay(String(newValue));
      setPreviousValue(newValue);
      onCalculate?.(newValue);
    }

    setWaitingForOperand(true);
    setOperation(nextOperation);
  };

  const calculate = (firstValue: number, secondValue: number, operation: string): number => {
    switch (operation) {
      case "+": return firstValue + secondValue;
      case "-": return firstValue - secondValue;
      case "×": return firstValue * secondValue;
      case "÷": return firstValue / secondValue;
      default: return secondValue;
    }
  };

  const performCalculation = () => {
    const inputValue = parseFloat(display);
    if (previousValue !== null && operation) {
      const newValue = calculate(previousValue, inputValue, operation);
      setDisplay(String(newValue));
      setPreviousValue(null);
      setOperation(null);
      setWaitingForOperand(true);
      onCalculate?.(newValue);
    }
  };

  const clear = () => {
    setDisplay("0");
    setPreviousValue(null);
    setOperation(null);
    setWaitingForOperand(false);
  };

  const Button = ({ onClick, className: buttonClassName, children, ...props }: any) => (
    <motion.button
      whileHover={{ scale: 1.05 }}
      whileTap={{ scale: 0.95 }}
      onClick={onClick}
      className={cn("h-16 text-xl font-semibold rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 transition-colors", buttonClassName)}
      {...props}
    >
      {children}
    </motion.button>
  );

  return (
    <div className={cn("bg-gray-100 p-6 rounded-2xl shadow-lg max-w-sm mx-auto", className)}>
      <div className="bg-gray-900 text-white p-4 rounded-lg mb-4 min-h-[4rem] flex items-center justify-end">
        <div className="text-3xl font-mono overflow-hidden text-ellipsis">{display}</div>
      </div>

      <div className="grid grid-cols-4 gap-3">
        <Button onClick={clear} className="col-span-2 bg-red-500 hover:bg-red-600 text-white">Clear</Button>
        <Button onClick={() => inputOperation("÷")} className="bg-orange-500 hover:bg-orange-600 text-white">÷</Button>
        <Button onClick={() => inputOperation("×")} className="bg-orange-500 hover:bg-orange-600 text-white">×</Button>

        <Button onClick={() => inputNumber("7")} className="bg-gray-300 hover:bg-gray-400 text-gray-800">7</Button>
        <Button onClick={() => inputNumber("8")} className="bg-gray-300 hover:bg-gray-400 text-gray-800">8</Button>
        <Button onClick={() => inputNumber("9")} className="bg-gray-300 hover:bg-gray-400 text-gray-800">9</Button>
        <Button onClick={() => inputOperation("-")} className="bg-orange-500 hover:bg-orange-600 text-white">-</Button>

        <Button onClick={() => inputNumber("4")} className="bg-gray-300 hover:bg-gray-400 text-gray-800">4</Button>
        <Button onClick={() => inputNumber("5")} className="bg-gray-300 hover:bg-gray-400 text-gray-800">5</Button>
        <Button onClick={() => inputNumber("6")} className="bg-gray-300 hover:bg-gray-400 text-gray-800">6</Button>
        <Button onClick={() => inputOperation("+")} className="bg-orange-500 hover:bg-orange-600 text-white">+</Button>

        <Button onClick={() => inputNumber("1")} className="bg-gray-300 hover:bg-gray-400 text-gray-800">1</Button>
        <Button onClick={() => inputNumber("2")} className="bg-gray-300 hover:bg-gray-400 text-gray-800">2</Button>
        <Button onClick={() => inputNumber("3")} className="bg-gray-300 hover:bg-gray-400 text-gray-800">3</Button>
        <Button onClick={performCalculation} className="row-span-2 bg-blue-500 hover:bg-blue-600 text-white">=</Button>

        <Button onClick={() => inputNumber("0")} className="col-span-2 bg-gray-300 hover:bg-gray-400 text-gray-800">0</Button>
        <Button onClick={() => inputNumber(".")} className="bg-gray-300 hover:bg-gray-400 text-gray-800">.</Button>
      </div>
    </div>
  );
}''',
        "dependencies": ["framer-motion", "clsx", "tailwind-merge"],
        "description": "Interactive calculator component with animations."
    }
}


@register_provider
class MagicUIProvider(GitHubProvider):
    """Magic UI component provider."""
    
    @property
    def provider_name(self) -> Provider:
        return Provider.MAGICUI
    
    @property
    def base_url(self) -> str:
        return "https://magicui.design"
    
    @property
    def github_repo(self) -> str:
        return "magicuidesign/magicui"
    
    async def list_components(
        self,
        limit: int = 50,
        offset: int = 0
    ) -> List[ComponentManifest]:
        """List Magic UI components from GitHub registry."""
        try:
            # Get registry file
            registry_content = await self.get_file_content("__registry__/registry.json")
            registry_data = json.loads(registry_content)
            
            components = []
            for component_data in registry_data.get("components", []):
                manifest = await self._create_manifest_from_registry(component_data)
                if manifest:
                    components.append(manifest)
            
            # Apply pagination
            start = offset
            end = offset + limit
            return components[start:end]
            
        except Exception as e:
            # Fallback to hardcoded components if registry is not available
            return await self._get_fallback_components()
    
    async def get_component(self, component_id: str) -> ComponentManifest:
        """Get specific Magic UI component."""
        # Remove provider prefix if present
        if "/" in component_id:
            component_id = component_id.split("/", 1)[1]
        
        components = await self.list_components(limit=1000)
        for component in components:
            if component.slug == component_id:
                return component
        
        raise ComponentNotFoundError(f"Component {component_id} not found in Magic UI")
    
    async def _create_manifest_from_registry(
        self,
        component_data: Dict[str, Any]
    ) -> Optional[ComponentManifest]:
        """Create component manifest from registry data with enhanced code templates."""
        try:
            name = component_data.get("name", "")
            slug = component_data.get("slug", name.lower().replace(" ", "-"))
            
            # Check if we have a template for this component
            template = MAGICUI_CODE_TEMPLATES.get(slug)
            code_content = ""
            runtime_deps = []
            
            if template:
                # Use our enhanced template
                code_content = template.get("tsx", "")
                runtime_deps = template.get("dependencies", [])
            else:
                # Try to get code from registry
                if "files" in component_data:
                    for file_info in component_data["files"]:
                        if file_info.get("type") == "component":
                            file_path = file_info.get("path", "")
                            if file_path:
                                try:
                                    code_content = await self.get_file_content(file_path)
                                    break
                                except:
                                    continue
                
                # Extract dependencies from code if no template
                if not runtime_deps:
                    runtime_deps = self._extract_dependencies(code_content)
            
            # Determine category
            category = self._determine_category(name, component_data.get("category", ""))
            
            return ComponentManifest(
                id=f"magicui/{slug}",
                provider=Provider.MAGICUI,
                name=name,
                slug=slug,
                category=category,
                tags=component_data.get("tags", []),
                license=License(
                    type=LicenseType.MIT,
                    url="https://github.com/magicuidesign/magicui/blob/main/LICENSE",
                    redistribute=True,
                    commercial=True
                ),
                source=Source(
                    url=f"https://github.com/magicuidesign/magicui/tree/main/{component_data.get('path', '')}",
                    commit=None,
                    branch="main"
                ),
                framework=Framework(
                    react=True,
                    next=True
                ),
                tailwind=TailwindConfig(
                    version=TailwindVersion.V4,
                    plugin_deps=[],
                    required_classes=self._extract_tailwind_classes(code_content)
                ),
                runtime_deps=runtime_deps,
                install=InstallPlan(
                    npm=runtime_deps,
                    steps=[]
                ),
                code=ComponentCode(
                    tsx=code_content if code_content else None
                ),
                access=ComponentAccess(
                    copy_paste=True,
                    cli=None,
                    pro=False
                ),
                description=component_data.get("description", ""),
                documentation_url=f"https://magicui.design/docs/components/{slug}",
                demo_url=f"https://magicui.design/docs/components/{slug}",
                keywords=component_data.get("keywords", [])
            )
            
        except Exception as e:
            print(f"Error creating manifest for {component_data}: {e}")
            return None
    
    def _extract_dependencies(self, code: str) -> List[str]:
        """Extract dependencies from component code."""
        deps = []
        
        # Common patterns for Magic UI components
        if "framer-motion" in code:
            deps.append("framer-motion")
        
        if "@radix-ui" in code:
            # Extract specific Radix UI packages
            radix_matches = re.findall(r'from ["\'](@radix-ui/[^"\']+)', code)
            deps.extend(radix_matches)
        
        if "lucide-react" in code:
            deps.append("lucide-react")
        
        if "class-variance-authority" in code:
            deps.append("class-variance-authority")
        
        if "clsx" in code:
            deps.append("clsx")
        
        if "tailwind-merge" in code:
            deps.append("tailwind-merge")
        
        return list(set(deps))  # Remove duplicates
    
    def _extract_tailwind_classes(self, code: str) -> List[str]:
        """Extract Tailwind classes from component code."""
        # This is a simplified extraction - in real implementation,
        # you'd want a more sophisticated parser
        classes = []
        
        # Look for className attributes
        class_matches = re.findall(r'className=["\']([^"\']+)["\']', code)
        for match in class_matches:
            # Split by spaces and filter Tailwind-like classes
            potential_classes = match.split()
            for cls in potential_classes:
                if self._is_tailwind_class(cls):
                    classes.append(cls)
        
        return list(set(classes))
    
    def _is_tailwind_class(self, cls: str) -> bool:
        """Check if a class looks like a Tailwind class."""
        # Simple heuristic - Tailwind classes often have specific patterns
        tailwind_patterns = [
            r'^(bg|text|border|p|m|w|h|flex|grid)-',
            r'^(hover|focus|active|disabled):',
            r'^(sm|md|lg|xl|2xl):',
            r'^animate-',
            r'^transition-'
        ]
        
        for pattern in tailwind_patterns:
            if re.match(pattern, cls):
                return True
        
        return False
    
    def _determine_category(self, name: str, registry_category: str) -> ComponentCategory:
        """Determine component category."""
        name_lower = name.lower()
        registry_lower = registry_category.lower()
        
        # Animation-related components
        if any(word in name_lower for word in ["marquee", "orbit", "particles", "typewriter", "blur"]):
            return ComponentCategory.ANIMATED
        
        # Text components
        if any(word in name_lower for word in ["text", "gradient", "word", "letter"]):
            return ComponentCategory.TEXT
        
        # Background components
        if any(word in name_lower for word in ["background", "grid", "dots", "meteors"]):
            return ComponentCategory.BACKGROUNDS
        
        # Layout components
        if any(word in name_lower for word in ["bento", "grid", "dock", "sidebar"]):
            return ComponentCategory.LAYOUTS
        
        # Form components
        if any(word in name_lower for word in ["input", "button", "form"]):
            return ComponentCategory.FORMS
        
        # Default based on registry category
        category_map = {
            "animation": ComponentCategory.ANIMATED,
            "layout": ComponentCategory.LAYOUTS,
            "form": ComponentCategory.FORMS,
            "text": ComponentCategory.TEXT,
            "background": ComponentCategory.BACKGROUNDS
        }
        
        return category_map.get(registry_lower, ComponentCategory.OTHER)
    
    async def _get_fallback_components(self) -> List[ComponentManifest]:
        """Get fallback components when registry is not available."""
        # Hardcoded popular Magic UI components
        fallback_components = [
            {
                "name": "Marquee",
                "slug": "marquee",
                "description": "An infinite scrolling component that can be used to display text, images, or any other content.",
                "category": "animated",
                "tags": ["animation", "scroll", "text"],
                "runtime_deps": ["framer-motion"]
            },
            {
                "name": "Orbit",
                "slug": "orbit",
                "description": "A component that displays content in an orbital animation.",
                "category": "animated", 
                "tags": ["animation", "orbit", "circular"],
                "runtime_deps": ["framer-motion"]
            },
            {
                "name": "Particles",
                "slug": "particles",
                "description": "A particle system component for creating dynamic backgrounds.",
                "category": "backgrounds",
                "tags": ["particles", "background", "animation"],
                "runtime_deps": ["framer-motion"]
            },
            {
                "name": "Gradient Text",
                "slug": "gradient-text",
                "description": "A text component with gradient effects.",
                "category": "text",
                "tags": ["text", "gradient", "styling"],
                "runtime_deps": []
            },
            {
                "name": "Blur Fade",
                "slug": "blur-fade",
                "description": "A component that creates blur and fade animations.",
                "category": "animated",
                "tags": ["animation", "blur", "fade"],
                "runtime_deps": ["framer-motion"]
            },
            {
                "name": "Animated Beam",
                "slug": "animated-beam",
                "description": "Animated beam connecting two elements with smooth transitions.",
                "category": "animated",
                "tags": ["animation", "beam", "connector"],
                "runtime_deps": ["framer-motion"]
            },
            {
                "name": "Magic Card",
                "slug": "magic-card",
                "description": "Interactive card with magical hover effects and animations.",
                "category": "cards",
                "tags": ["card", "hover", "interactive"],
                "runtime_deps": ["framer-motion"]
            },
            {
                "name": "Number Ticker",
                "slug": "number-ticker",
                "description": "Animated number counter with smooth transitions and customizable formatting.",
                "category": "animated",
                "tags": ["counter", "animation", "numbers"],
                "runtime_deps": ["framer-motion"]
            },
            {
                "name": "Globe",
                "slug": "globe",
                "description": "Interactive 3D globe component with customizable markers and animations.",
                "category": "data_display",
                "tags": ["3d", "globe", "interactive"],
                "runtime_deps": ["three", "framer-motion"]
            },
            {
                "name": "Sparkles",
                "slug": "sparkles",
                "description": "Magical sparkle animation effect for highlighting content.",
                "category": "animated",
                "tags": ["sparkle", "animation", "magic"],
                "runtime_deps": ["framer-motion"]
            },
            {
                "name": "Meteors",
                "slug": "meteors",
                "description": "Animated meteors falling across the screen as background effect.",
                "category": "backgrounds",
                "tags": ["meteors", "animation", "background"],
                "runtime_deps": ["framer-motion"]
            },
            {
                "name": "Ripple",
                "slug": "ripple",
                "description": "Ripple effect animation component for interactions.",
                "category": "animated",
                "tags": ["ripple", "animation", "effect"],
                "runtime_deps": ["framer-motion"]
            },
            {
                "name": "Dock",
                "slug": "dock",
                "description": "MacOS-style dock navigation component with spring animations.",
                "category": "navigation",
                "tags": ["dock", "navigation", "macos"],
                "runtime_deps": ["framer-motion"]
            },
            {
                "name": "Avatar Circles",
                "slug": "avatar-circles",
                "description": "Circular avatar layout component with hover animations.",
                "category": "data_display",
                "tags": ["avatar", "circle", "profile"],
                "runtime_deps": ["framer-motion"]
            },
            {
                "name": "Border Beam",
                "slug": "border-beam",
                "description": "Animated border with moving beam effect for highlighting elements.",
                "category": "animated",
                "tags": ["border", "beam", "animation"],
                "runtime_deps": ["framer-motion"]
            },
            {
                "name": "Typing Animation",
                "slug": "typing-animation",
                "description": "Typewriter effect text animation with customizable speed.",
                "category": "text",
                "tags": ["typing", "text", "animation"],
                "runtime_deps": ["framer-motion"]
            },
            {
                "name": "Word Rotate",
                "slug": "word-rotate",
                "description": "Rotating word animation component for dynamic text display.",
                "category": "text",
                "tags": ["word", "rotate", "animation"],
                "runtime_deps": ["framer-motion"]
            },
            {
                "name": "Flickering Grid",
                "slug": "flickering-grid",
                "description": "Grid with flickering light effects for cyberpunk aesthetics.",
                "category": "backgrounds",
                "tags": ["grid", "flicker", "animation"],
                "runtime_deps": ["framer-motion"]
            },
            {
                "name": "Bento Grid",
                "slug": "bento-grid",
                "description": "Masonry-style bento box grid layout for content organization.",
                "category": "layouts",
                "tags": ["grid", "layout", "bento"],
                "runtime_deps": []
            },
            {
                "name": "Animated Shiny Text",
                "slug": "animated-shiny-text",
                "description": "Text with animated shiny effect and gradient overlay.",
                "category": "text",
                "tags": ["text", "shine", "animation"],
                "runtime_deps": ["framer-motion"]
            },
            {
                "name": "Magic Button",
                "slug": "magic-button",
                "description": "Button with magical hover animations and particle effects.",
                "category": "inputs",
                "tags": ["button", "magic", "hover"],
                "runtime_deps": ["framer-motion"]
            },
            {
                "name": "Shimmer",
                "slug": "shimmer",
                "description": "Shimmer loading effect component for skeleton screens.",
                "category": "feedback",
                "tags": ["shimmer", "loading", "effect"],
                "runtime_deps": ["framer-motion"]
            },
            {
                "name": "Rainbow Button",
                "slug": "rainbow-button",
                "description": "Button with rainbow gradient animation and hover effects.",
                "category": "inputs",
                "tags": ["button", "rainbow", "gradient"],
                "runtime_deps": ["framer-motion"]
            },
            {
                "name": "Text Reveal",
                "slug": "text-reveal",
                "description": "Text reveal animation triggered on scroll or hover.",
                "category": "text",
                "tags": ["text", "reveal", "scroll"],
                "runtime_deps": ["framer-motion"]
            },
            {
                "name": "Animated List",
                "slug": "animated-list",
                "description": "List with staggered item animations and smooth transitions.",
                "category": "data_display",
                "tags": ["list", "stagger", "animation"],
                "runtime_deps": ["framer-motion"]
            },
            {
                "name": "Cool Mode",
                "slug": "cool-mode",
                "description": "Cool particle effect triggered on user interactions.",
                "category": "animated",
                "tags": ["cool", "particles", "interaction"],
                "runtime_deps": ["framer-motion"]
            },
            {
                "name": "Neon Glow",
                "slug": "neon-glow",
                "description": "Neon glow effect for elements with customizable colors.",
                "category": "animated",
                "tags": ["neon", "glow", "effect"],
                "runtime_deps": []
            },
            {
                "name": "Confetti",
                "slug": "confetti",
                "description": "Celebration confetti animation with physics simulation.",
                "category": "animated",
                "tags": ["confetti", "celebration", "animation"],
                "runtime_deps": ["canvas-confetti", "framer-motion"]
            },
            {
                "name": "Spotlight",
                "slug": "spotlight",
                "description": "Interactive spotlight effect that follows cursor movement.",
                "category": "animated",
                "tags": ["spotlight", "effect", "interactive"],
                "runtime_deps": ["framer-motion"]
            },
            {
                "name": "Liquid Blob",
                "slug": "liquid-blob",
                "description": "Morphing liquid blob animation with smooth transitions.",
                "category": "animated",
                "tags": ["blob", "liquid", "morph"],
                "runtime_deps": ["framer-motion"]
            },
            {
                "name": "Contact Form",
                "slug": "contact-form",
                "description": "A complete contact form with validation, loading states, and success feedback.",
                "category": "forms",
                "tags": ["form", "contact", "validation"],
                "runtime_deps": ["framer-motion"]
            },
            {
                "name": "Modal Dialog",
                "slug": "modal-dialog",
                "description": "A flexible modal dialog component with animations and keyboard support.",
                "category": "overlays",
                "tags": ["modal", "dialog", "overlay"],
                "runtime_deps": ["framer-motion"]
            },
            {
                "name": "Image Gallery",
                "slug": "image-gallery",
                "description": "Interactive image gallery with lightbox functionality.",
                "category": "data_display",
                "tags": ["gallery", "images", "lightbox"],
                "runtime_deps": ["framer-motion"]
            },
            {
                "name": "Loading Spinner",
                "slug": "loading-spinner",
                "description": "Animated loading spinner with multiple variants.",
                "category": "feedback",
                "tags": ["loading", "spinner", "feedback"],
                "runtime_deps": ["framer-motion"]
            },
            {
                "name": "Tooltip",
                "slug": "tooltip",
                "description": "Interactive tooltip component with positioning.",
                "category": "overlays",
                "tags": ["tooltip", "hover", "info"],
                "runtime_deps": ["framer-motion"]
            },
            {
                "name": "Calculator",
                "slug": "calculator",
                "description": "Interactive calculator component with animations.",
                "category": "other",
                "tags": ["calculator", "math", "interactive"],
                "runtime_deps": ["framer-motion"]
            }
        ]
        
        components = []
        for comp_data in fallback_components:
            manifest = ComponentManifest(
                id=f"magicui/{comp_data['slug']}",
                provider=Provider.MAGICUI,
                name=comp_data["name"],
                slug=comp_data["slug"],
                category=ComponentCategory(comp_data["category"]),
                tags=comp_data["tags"],
                license=License(
                    type=LicenseType.MIT,
                    url="https://github.com/magicuidesign/magicui/blob/main/LICENSE",
                    redistribute=True,
                    commercial=True
                ),
                source=Source(
                    url=f"https://github.com/magicuidesign/magicui",
                    branch="main"
                ),
                framework=Framework(
                    react=True,
                    next=True
                ),
                tailwind=TailwindConfig(
                    version=TailwindVersion.V4,
                    plugin_deps=[]
                ),
                runtime_deps=comp_data["runtime_deps"],
                install=InstallPlan(
                    npm=comp_data["runtime_deps"]
                ),
                code=ComponentCode(
                    tsx=MAGICUI_CODE_TEMPLATES.get(comp_data['slug'], {}).get('tsx')
                ),
                access=ComponentAccess(
                    copy_paste=True,
                    pro=False
                ),
                description=comp_data["description"],
                documentation_url=f"https://magicui.design/docs/components/{comp_data['slug']}",
                demo_url=f"https://magicui.design/docs/components/{comp_data['slug']}"
            )
            components.append(manifest)
        
        return components