import React from 'react';
import { ArrowRight, Star } from 'lucide-react';

export default function Hero() {
  return (
    <div className="relative bg-gradient-to-br from-blue-600 via-purple-600 to-indigo-700 overflow-hidden">
      <div className="absolute inset-0 bg-black opacity-10"></div>
      <div className="max-w-7xl mx-auto">
        <div className="relative z-10 pb-8 sm:pb-16 md:pb-20 lg:max-w-2xl lg:w-full lg:pb-28 xl:pb-32">
          <main className="mt-10 mx-auto max-w-7xl px-4 sm:mt-12 sm:px-6 md:mt-16 lg:mt-20 lg:px-8 xl:mt-28">
            <div className="sm:text-center lg:text-left">
              <div className="flex items-center mb-6 sm:justify-center lg:justify-start">
                <div className="flex items-center bg-yellow-100 rounded-full px-3 py-1">
                  <Star className="h-4 w-4 text-yellow-500 mr-1" />
                  <span className="text-sm text-yellow-800 font-medium">New: 11 UI Libraries</span>
                </div>
              </div>
              
              <h1 className="text-4xl tracking-tight font-extrabold text-white sm:text-5xl md:text-6xl">
                <span className="block xl:inline">UI Components</span>{' '}
                <span className="block text-yellow-400 xl:inline">Made Simple</span>
              </h1>
              
              <p className="mt-3 text-base text-gray-100 sm:mt-5 sm:text-lg sm:max-w-xl sm:mx-auto md:mt-5 md:text-xl lg:mx-0">
                Access thousands of beautiful, ready-to-use UI components from the best design systems.
                Copy, paste, and customize in seconds with AI-powered recommendations.
              </p>
              
              <div className="mt-5 sm:mt-8 sm:flex sm:justify-center lg:justify-start">
                <div className="rounded-md shadow">
                  <a
                    href="#"
                    className="w-full flex items-center justify-center px-8 py-3 border border-transparent text-base font-medium rounded-md text-blue-700 bg-white hover:bg-gray-50 md:py-4 md:text-lg md:px-10 transition-colors"
                  >
                    Get Started
                    <ArrowRight className="ml-2 h-5 w-5" />
                  </a>
                </div>
                <div className="mt-3 sm:mt-0 sm:ml-3">
                  <a
                    href="#"
                    className="w-full flex items-center justify-center px-8 py-3 border border-transparent text-base font-medium rounded-md text-white bg-blue-500 hover:bg-blue-600 md:py-4 md:text-lg md:px-10 transition-colors"
                  >
                    Browse Components
                  </a>
                </div>
              </div>
              
              <div className="mt-8 flex items-center sm:justify-center lg:justify-start space-x-6">
                <div className="flex items-center text-gray-200">
                  <span className="text-2xl font-bold text-white">326</span>
                  <span className="ml-2 text-sm">Components</span>
                </div>
                <div className="flex items-center text-gray-200">
                  <span className="text-2xl font-bold text-white">11</span>
                  <span className="ml-2 text-sm">Providers</span>
                </div>
                <div className="flex items-center text-gray-200">
                  <span className="text-2xl font-bold text-white">100%</span>
                  <span className="ml-2 text-sm">Free</span>
                </div>
              </div>
            </div>
          </main>
        </div>
      </div>
    </div>
  );
}