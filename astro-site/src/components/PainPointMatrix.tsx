import React, { useState } from 'react';

interface PainPoint {
  category: string;
  aps: string;
  onshape: string;
  solidworks: string;
  teamcenter: string;
  nxOpen: string;
}

const painPoints: PainPoint[] = [
  {
    category: 'OAuth Complexity',
    aps: 'HIGH',
    onshape: 'HIGH',
    solidworks: 'MEDIUM',
    teamcenter: 'HIGH',
    nxOpen: 'N/A',
  },
  {
    category: 'Token Handling',
    aps: 'HIGH',
    onshape: 'HIGH',
    solidworks: 'N/A',
    teamcenter: 'HIGH',
    nxOpen: 'N/A',
  },
  {
    category: 'File Translation',
    aps: 'HIGH',
    onshape: 'HIGH',
    solidworks: 'HIGH',
    teamcenter: 'MEDIUM-HIGH',
    nxOpen: 'MEDIUM',
  },
  {
    category: 'Large File Failures',
    aps: 'HIGH',
    onshape: 'HIGH',
    solidworks: 'HIGH',
    teamcenter: 'MEDIUM',
    nxOpen: 'MEDIUM',
  },
  {
    category: 'SDK Version Conflicts',
    aps: 'HIGH',
    onshape: 'MEDIUM',
    solidworks: 'CRITICAL',
    teamcenter: 'HIGH',
    nxOpen: 'HIGH',
  },
  {
    category: 'Documentation Gaps',
    aps: 'MEDIUM',
    onshape: 'MEDIUM',
    solidworks: 'HIGH',
    teamcenter: 'CRITICAL',
    nxOpen: 'CRITICAL',
  },
  {
    category: 'Missing Examples',
    aps: 'HIGH',
    onshape: 'MEDIUM',
    solidworks: 'HIGH',
    teamcenter: 'HIGH',
    nxOpen: 'HIGH',
  },
  {
    category: 'Webhook Reliability',
    aps: 'MEDIUM',
    onshape: 'HIGH',
    solidworks: 'NEW',
    teamcenter: 'MEDIUM',
    nxOpen: 'N/A',
  },
  {
    category: 'Error Code Clarity',
    aps: 'MEDIUM',
    onshape: 'MEDIUM',
    solidworks: 'HIGH',
    teamcenter: 'HIGH',
    nxOpen: 'MEDIUM-HIGH',
  },
];

const getSeverityColor = (severity: string): string => {
  switch (severity) {
    case 'CRITICAL':
      return 'bg-red-500 text-white';
    case 'HIGH':
      return 'bg-orange-500 text-white';
    case 'MEDIUM-HIGH':
      return 'bg-orange-400 text-white';
    case 'MEDIUM':
      return 'bg-yellow-400 text-gray-900';
    case 'NEW':
      return 'bg-green-400 text-white';
    case 'N/A':
      return 'bg-gray-200 text-gray-500';
    default:
      return 'bg-gray-100';
  }
};

export const PainPointMatrix: React.FC = () => {
  const [selectedPlatform, setSelectedPlatform] = useState<string | null>(null);
  const [hoveredCell, setHoveredCell] = useState<{ row: number; col: string } | null>(null);

  const platforms = ['aps', 'onshape', 'solidworks', 'teamcenter', 'nxOpen'];
  const platformNames = {
    aps: 'Autodesk APS',
    onshape: 'PTC Onshape',
    solidworks: 'SOLIDWORKS',
    teamcenter: 'Teamcenter',
    nxOpen: 'NX Open',
  };

  return (
    <div className="w-full">
      <div className="mb-6 flex flex-wrap gap-2">
        <button
          onClick={() => setSelectedPlatform(null)}
          className={`px-3 py-1 rounded-lg transition ${
            selectedPlatform === null
              ? 'bg-gradient-to-r from-raps-blue to-raps-purple text-white'
              : 'bg-gray-100 hover:bg-gray-200'
          }`}
        >
          All Platforms
        </button>
        {platforms.map((platform) => (
          <button
            key={platform}
            onClick={() => setSelectedPlatform(platform)}
            className={`px-3 py-1 rounded-lg transition ${
              selectedPlatform === platform
                ? 'bg-gradient-to-r from-raps-blue to-raps-purple text-white'
                : 'bg-gray-100 hover:bg-gray-200'
            }`}
          >
            {platformNames[platform as keyof typeof platformNames]}
          </button>
        ))}
      </div>

      <div className="overflow-x-auto">
        <table className="w-full border-collapse">
          <thead>
            <tr>
              <th className="text-left p-3 bg-gray-900 text-white font-semibold sticky left-0 z-10">
                Pain Point
              </th>
              {platforms.map((platform) => (
                <th
                  key={platform}
                  className={`p-3 bg-gray-800 text-white font-semibold text-center transition ${
                    selectedPlatform && selectedPlatform !== platform ? 'opacity-50' : ''
                  }`}
                >
                  {platformNames[platform as keyof typeof platformNames]}
                </th>
              ))}
            </tr>
          </thead>
          <tbody>
            {painPoints.map((point, idx) => (
              <tr key={idx} className="border-b border-gray-200">
                <td className="p-3 font-medium bg-gray-50 sticky left-0">
                  {point.category}
                </td>
                {platforms.map((platform) => {
                  const value = point[platform as keyof PainPoint];
                  const isHighlighted = selectedPlatform === null || selectedPlatform === platform;
                  const isHovered = hoveredCell?.row === idx && hoveredCell?.col === platform;

                  return (
                    <td
                      key={platform}
                      className={`p-3 text-center transition-all ${
                        !isHighlighted ? 'opacity-30' : ''
                      }`}
                      onMouseEnter={() => setHoveredCell({ row: idx, col: platform })}
                      onMouseLeave={() => setHoveredCell(null)}
                    >
                      <span
                        className={`inline-block px-3 py-1 rounded-md font-semibold text-sm transition-transform ${
                          getSeverityColor(value)
                        } ${isHovered ? 'scale-110 shadow-lg' : ''}`}
                      >
                        {value}
                      </span>
                    </td>
                  );
                })}
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      <div className="mt-6 p-4 bg-blue-50 rounded-lg">
        <h4 className="font-semibold text-blue-900 mb-2">Key Insights:</h4>
        <ul className="space-y-1 text-sm text-blue-800">
          <li>• SOLIDWORKS has CRITICAL SDK version conflicts (annual rebuilds required)</li>
          <li>• Teamcenter and NX Open have CRITICAL documentation gaps</li>
          <li>• Authentication complexity affects ALL platforms equally</li>
          <li>• File translation issues are universal across the industry</li>
        </ul>
      </div>
    </div>
  );
};