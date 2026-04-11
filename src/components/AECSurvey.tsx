import { useState } from 'react';

interface SurveyData {
  role: string;
  companySize: string;
  accUsage: string;
  painPoints: string[];
  email: string;
}

const PAIN_POINTS = [
  'Manual user provisioning across projects',
  'Permission management at scale',
  'Compliance and audit requirements',
  'Slow project setup and configuration',
  'No bulk operations for ACC',
  'Difficulty migrating between ACC accounts',
  'Lack of automation tooling',
  'Other',
];

export default function AECSurvey() {
  const [step, setStep] = useState(0);
  const [data, setData] = useState<SurveyData>({
    role: '',
    companySize: '',
    accUsage: '',
    painPoints: [],
    email: '',
  });
  const [submitted, setSubmitted] = useState(false);

  const update = (field: keyof SurveyData, value: string | string[]) => {
    setData((prev) => ({ ...prev, [field]: value }));
  };

  const togglePainPoint = (point: string) => {
    setData((prev) => ({
      ...prev,
      painPoints: prev.painPoints.includes(point)
        ? prev.painPoints.filter((p) => p !== point)
        : [...prev.painPoints, point],
    }));
  };

  const submit = async () => {
    try {
      await fetch('/api/survey', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data),
      });
    } catch {
      // Best-effort submission
    }
    setSubmitted(true);
  };

  if (submitted) {
    return (
      <div className="text-center py-16 px-4">
        <div className="text-6xl mb-6">🙏</div>
        <h2 className="text-3xl font-bold mb-4">Thank you!</h2>
        <p className="text-lg text-gray-600 mb-8 max-w-md mx-auto">
          Your responses help us build better AEC automation tools.
          We'll share the results with the community.
        </p>
        <a href="/" className="inline-block px-6 py-3 bg-gradient-to-r from-purple-600 to-blue-500 text-white rounded-lg font-medium hover:shadow-lg transition-all">
          Back to rapscli.xyz
        </a>
      </div>
    );
  }

  const steps = [
    // Step 0: Role
    <div key="role">
      <h2 className="text-2xl font-bold mb-2">What's your role?</h2>
      <p className="text-gray-600 mb-6">Help us understand who's automating AEC workflows.</p>
      <div className="space-y-3">
        {['BIM Manager', 'IT Administrator', 'Developer', 'Project Manager', 'Other'].map((role) => (
          <button
            key={role}
            onClick={() => { update('role', role); setStep(1); }}
            className={`w-full text-left px-4 py-3 rounded-lg border transition ${
              data.role === role ? 'border-purple-500 bg-purple-50' : 'border-gray-200 hover:border-gray-300'
            }`}
          >
            {role}
          </button>
        ))}
      </div>
    </div>,

    // Step 1: Company size
    <div key="size">
      <h2 className="text-2xl font-bold mb-2">Company size?</h2>
      <p className="text-gray-600 mb-6">This helps us tailor recommendations.</p>
      <div className="space-y-3">
        {['1-50 employees', '51-200', '201-1000', '1000+'].map((size) => (
          <button
            key={size}
            onClick={() => { update('companySize', size); setStep(2); }}
            className={`w-full text-left px-4 py-3 rounded-lg border transition ${
              data.companySize === size ? 'border-purple-500 bg-purple-50' : 'border-gray-200 hover:border-gray-300'
            }`}
          >
            {size}
          </button>
        ))}
      </div>
    </div>,

    // Step 2: ACC usage
    <div key="usage">
      <h2 className="text-2xl font-bold mb-2">How many ACC projects do you manage?</h2>
      <p className="text-gray-600 mb-6">Understanding your scale helps us prioritize features.</p>
      <div className="space-y-3">
        {['Not using ACC yet', '1-20 projects', '21-100 projects', '100-500 projects', '500+ projects'].map((usage) => (
          <button
            key={usage}
            onClick={() => { update('accUsage', usage); setStep(3); }}
            className={`w-full text-left px-4 py-3 rounded-lg border transition ${
              data.accUsage === usage ? 'border-purple-500 bg-purple-50' : 'border-gray-200 hover:border-gray-300'
            }`}
          >
            {usage}
          </button>
        ))}
      </div>
    </div>,

    // Step 3: Pain points
    <div key="pain">
      <h2 className="text-2xl font-bold mb-2">What are your biggest pain points?</h2>
      <p className="text-gray-600 mb-6">Select all that apply.</p>
      <div className="space-y-3 mb-6">
        {PAIN_POINTS.map((point) => (
          <button
            key={point}
            onClick={() => togglePainPoint(point)}
            className={`w-full text-left px-4 py-3 rounded-lg border transition ${
              data.painPoints.includes(point) ? 'border-purple-500 bg-purple-50' : 'border-gray-200 hover:border-gray-300'
            }`}
          >
            <span className="mr-2">{data.painPoints.includes(point) ? '✓' : '○'}</span>
            {point}
          </button>
        ))}
      </div>
      <button
        onClick={() => setStep(4)}
        disabled={data.painPoints.length === 0}
        className="w-full px-6 py-3 bg-gradient-to-r from-purple-600 to-blue-500 text-white rounded-lg font-medium hover:shadow-lg transition-all disabled:opacity-50 disabled:cursor-not-allowed"
      >
        Continue
      </button>
    </div>,

    // Step 4: Email
    <div key="email">
      <h2 className="text-2xl font-bold mb-2">Stay in the loop</h2>
      <p className="text-gray-600 mb-6">Get the survey results and early access to new tools. Optional.</p>
      <input
        type="email"
        placeholder="you@company.com"
        value={data.email}
        onChange={(e) => update('email', e.target.value)}
        className="w-full px-4 py-3 border border-gray-200 rounded-lg mb-4 outline-none focus:ring-2 focus:ring-purple-500 focus:border-transparent"
      />
      <div className="flex gap-3">
        <button
          onClick={submit}
          className="flex-1 px-6 py-3 bg-gradient-to-r from-purple-600 to-blue-500 text-white rounded-lg font-medium hover:shadow-lg transition-all"
        >
          Submit
        </button>
        <button
          onClick={submit}
          className="px-6 py-3 text-gray-500 hover:text-gray-700 transition"
        >
          Skip
        </button>
      </div>
    </div>,
  ];

  return (
    <div className="max-w-lg mx-auto px-4 py-12">
      {/* Progress */}
      <div className="flex gap-2 mb-8">
        {steps.map((_, i) => (
          <div
            key={i}
            className={`h-1 flex-1 rounded-full transition ${
              i <= step ? 'bg-gradient-to-r from-purple-600 to-blue-500' : 'bg-gray-200'
            }`}
          />
        ))}
      </div>

      {/* Back button */}
      {step > 0 && (
        <button
          onClick={() => setStep(step - 1)}
          className="text-sm text-gray-500 hover:text-gray-700 mb-4 flex items-center transition"
        >
          <svg className="w-4 h-4 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 19l-7-7 7-7" />
          </svg>
          Back
        </button>
      )}

      {steps[step]}
    </div>
  );
}
