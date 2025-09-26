import React from 'react';
import { Check, X } from 'lucide-react';

const plans = [
  {
    name: 'Free',
    price: '$0',
    description: 'Perfect for getting started',
    features: [
      { name: 'Access to basic components', included: true },
      { name: 'Copy & paste code', included: true },
      { name: 'Community support', included: true },
      { name: 'MIT licensed components', included: true },
      { name: 'Premium components', included: false },
      { name: 'Priority support', included: false },
    ],
    cta: 'Get Started',
    popular: false
  },
  {
    name: 'Pro',
    price: '$29',
    description: 'For professional developers',
    features: [
      { name: 'Access to all components', included: true },
      { name: 'Premium blocks & templates', included: true },
      { name: 'Priority support', included: true },
      { name: 'Commercial license', included: true },
      { name: 'Advanced customization', included: true },
      { name: 'Private component library', included: false },
    ],
    cta: 'Start Free Trial',
    popular: true
  },
  {
    name: 'Team',
    price: '$99',
    description: 'For growing teams',
    features: [
      { name: 'Everything in Pro', included: true },
      { name: 'Team collaboration', included: true },
      { name: 'Private component library', included: true },
      { name: 'Design system tools', included: true },
      { name: 'SSO integration', included: true },
      { name: 'Custom integrations', included: true },
    ],
    cta: 'Contact Sales',
    popular: false
  }
];

export default function PricingTable() {
  return (
    <div className="py-12 bg-gray-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="text-center">
          <h2 className="text-3xl font-extrabold text-gray-900 sm:text-4xl">
            Simple, transparent pricing
          </h2>
          <p className="mt-4 text-xl text-gray-600">
            Choose the plan that works for you
          </p>
        </div>
        
        <div className="mt-12 space-y-4 sm:mt-16 sm:space-y-0 sm:grid sm:grid-cols-3 sm:gap-6 lg:max-w-4xl lg:mx-auto">
          {plans.map((plan) => (
            <div
              key={plan.name}
              className={`relative p-8 bg-white border rounded-lg shadow-sm ${
                plan.popular ? 'border-blue-500 ring-2 ring-blue-500' : 'border-gray-200'
              }`}
            >
              {plan.popular && (
                <div className="absolute top-0 right-6 transform -translate-y-1/2">
                  <span className="inline-flex px-4 py-1 text-sm font-semibold text-white bg-blue-500 rounded-full">
                    Most Popular
                  </span>
                </div>
              )}
              
              <div className="text-center">
                <h3 className="text-2xl font-semibold text-gray-900">{plan.name}</h3>
                <p className="mt-2 text-gray-500">{plan.description}</p>
                <div className="mt-4">
                  <span className="text-4xl font-extrabold text-gray-900">{plan.price}</span>
                  <span className="text-base font-medium text-gray-500">/month</span>
                </div>
              </div>
              
              <ul className="mt-8 space-y-4">
                {plan.features.map((feature) => (
                  <li key={feature.name} className="flex items-start">
                    <div className="flex-shrink-0">
                      {feature.included ? (
                        <Check className="h-6 w-6 text-green-500" />
                      ) : (
                        <X className="h-6 w-6 text-gray-300" />
                      )}
                    </div>
                    <p className={`ml-3 text-base ${feature.included ? 'text-gray-700' : 'text-gray-400'}`}>
                      {feature.name}
                    </p>
                  </li>
                ))}
              </ul>
              
              <div className="mt-8">
                <button
                  className={`w-full py-3 px-6 border border-transparent rounded-md text-center font-medium transition-colors ${
                    plan.popular
                      ? 'text-white bg-blue-600 hover:bg-blue-700'
                      : 'text-blue-600 bg-blue-50 hover:bg-blue-100'
                  }`}
                >
                  {plan.cta}
                </button>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}