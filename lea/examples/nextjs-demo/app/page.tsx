import React from 'react';
import NavigationBar from '../components/NavigationBar';
import HeroSection from '../components/HeroSection';
import PricingTable from '../components/PricingTable';
import AuthenticationForm from '../components/AuthenticationForm';
import './globals.css';

export default function HomePage() {
  return (
    <div className="min-h-screen bg-gray-50">
      <NavigationBar />
      <HeroSection />
      <div className="py-16">
        <div className="max-w-4xl mx-auto px-4">
          <h2 className="text-3xl font-bold text-center mb-12">Choose Your Plan</h2>
          <PricingTable />
        </div>
      </div>
      <div className="py-16 bg-white">
        <div className="max-w-4xl mx-auto px-4">
          <h2 className="text-3xl font-bold text-center mb-12">Sign In</h2>
          <AuthenticationForm />
        </div>
      </div>
    </div>
  );
}