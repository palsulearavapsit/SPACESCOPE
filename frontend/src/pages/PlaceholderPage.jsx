import React from 'react';

const pages = [
  'EventCalendar',
  'SpaceWeather',
  'Missions',
  'LearningZone',
  'EarthImpact',
];

export default function PlaceholderPage({ name }) {
  return (
    <div className="text-center py-20">
      <h1 className="text-4xl font-bold text-indigo-400 mb-4">{name}</h1>
      <p className="text-gray-400">Coming soon...</p>
    </div>
  );
}

// Generate placeholder pages
pages.forEach((page) => {
  const fileName = page;
  const componentCode = `import React from 'react';
import PlaceholderPage from '../components/PlaceholderPage';

function ${page}() {
  return <PlaceholderPage name="${page}" />;
}

export default ${page};
`;
});
