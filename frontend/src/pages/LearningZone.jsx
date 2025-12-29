import React, { useEffect, useState } from 'react';
import { learningAPI } from '../services/api';
import { FaBook, FaStar, FaPlayCircle, FaAward } from 'react-icons/fa';
import DetailModal from '../components/DetailModal';
import LessonModal from '../components/LessonModal';

function LearningZone() {
  const [content, setContent] = useState([]);
  const [category, setCategory] = useState(null);
  const [difficulty, setDifficulty] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [selectedCourse, setSelectedCourse] = useState(null);
  const [selectedLesson, setSelectedLesson] = useState(null);

  useEffect(() => {
    loadContent();
  }, [category, difficulty]);

  const loadContent = async () => {
    try {
      setLoading(true);
      const response = await learningAPI.getContent(category, difficulty);
      setContent(response.data || []);
      setError(null);
    } catch (err) {
      console.error('Error loading content:', err);
      setError('Failed to load learning content');
      setContent([]);
    } finally {
      setLoading(false);
    }
  };

  const mockContent = [
    // ===== PLANETS CATEGORY =====
    // BEGINNER
    {
      id: 1,
      title: 'Planets 101: Solar System Basics',
      category: 'Planets',
      difficulty: 'Beginner',
      duration: '14 min',
      description: 'Learn the fundamentals of our solar system and planetary characteristics.',
      rating: 4.9,
      students: 9100,
      fullDescription: 'A foundational guide to planets. Explore what makes a planet, orbital mechanics basics, and the unique characteristics of our eight planets.',
      lessons: [
        { name: 'What Defines a Planet?', duration: '2 min', content: 'Learn the scientific definition of a planet according to the International Astronomical Union. Discover why Pluto was reclassified and what the three criteria for planetary status are: orbiting the sun, being massive enough to be round, and clearing its orbital path.' },
        { name: 'Orbital Mechanics', duration: '2 min', content: 'Understand how planets orbit the sun in elliptical paths. Learn about Kepler\'s laws of planetary motion, orbital periods, and how distance from the sun affects orbital velocity.' },
        { name: 'Planetary Types', duration: '2 min', content: 'Explore the two main types of planets: terrestrial (rocky) planets like Earth and Mars, and gas giants like Jupiter and Saturn. Understand their different compositions and characteristics.' },
        { name: 'Moon Systems', duration: '2 min', content: 'Discover how many moons each planet has and why some planets have many moons while others have none. Learn about the largest moons in our solar system and their unique features.' },
        { name: 'Asteroid Belts', duration: '2 min', content: 'Understand asteroid belts between planets, including our own asteroid belt between Mars and Jupiter. Learn how asteroids formed and their importance to planetary science.' },
        { name: 'Formation Theory', duration: '2 min', content: 'Study how our solar system formed from a solar nebula approximately 4.6 billion years ago. Learn about planetary accretion and migration.' }
      ],
      instructor: 'Dr. Emily Rodriguez',
      prerequisites: 'None - beginner friendly'
    },
    {
      id: 2,
      title: 'Exoplanets and Habitable Zones',
      category: 'Planets',
      difficulty: 'Beginner',
      duration: '15 min',
      description: 'Discover how astronomers find planets around other stars.',
      rating: 4.9,
      students: 8900,
      fullDescription: 'Learn about exoplanet discovery methods and habitable zones. Understand how we detect planets and which might harbor life.',
      lessons: [
        { name: 'Detection Methods', duration: '2 min', content: 'Explore the primary techniques used to detect exoplanets: the transit method, radial velocity method, and direct imaging. Understand how each method works and their advantages.' },
        { name: 'Transit Method', duration: '2 min', content: 'Learn how this most successful detection method works by observing the dimming of starlight when a planet passes in front of its star. Understand how we measure planetary radius and composition.' },
        { name: 'Radial Velocity', duration: '2 min', content: 'Discover how stars "wobble" due to orbiting planets. Learn how we measure this wobble using Doppler shift to determine planet mass and orbital characteristics.' },
        { name: 'Habitable Zones', duration: '2 min', content: 'Understand the "Goldilocks zone" where conditions are right for liquid water. Learn about stellar habitable zones and factors that determine if a planet could support life.' },
        { name: 'Notable Exoplanets', duration: '2 min', content: 'Explore famous exoplanet discoveries like Proxima Centauri b, the TRAPPIST-1 system, and Kepler-452b. Learn their characteristics and why they\'re particularly interesting.' },
        { name: 'Future Missions', duration: '2 min', content: 'Discover upcoming exoplanet hunting missions like the James Webb Space Telescope and future direct imaging telescopes that will revolutionize our search for habitable worlds.' }
      ],
      instructor: 'Dr. Sarah Mitchell',
      prerequisites: 'None - completely beginner friendly'
    },
    // INTERMEDIATE
    {
      id: 3,
      title: 'The Inner and Outer Planets',
      category: 'Planets',
      difficulty: 'Intermediate',
      duration: '22 min',
      description: 'Explore the characteristics and histories of all planets.',
      rating: 4.7,
      students: 7100,
      fullDescription: 'A comprehensive tour of our solar system. Learn about terrestrial and gas giant planets, their atmospheres, and recent discoveries.',
      lessons: [
        { name: 'Terrestrial Planets', duration: '3 min', content: 'Study the four inner rocky planets: Mercury, Venus, Earth, and Mars. Learn about their geology, atmospheres, temperatures, and potential for habitability.' },
        { name: 'Gas Giants', duration: '4 min', content: 'Explore Jupiter and Saturn - the massive gas giants with complex atmospheres, powerful storms, and extensive moon systems.' },
        { name: 'Ice Giants', duration: '3 min', content: 'Discover Uranus and Neptune, the outer ice giants with methane atmospheres, extreme winds, and mysterious interiors.' },
        { name: 'Atmospheres', duration: '3 min', content: 'Compare planetary atmospheres from thin to thick. Understand atmospheric composition, pressure, temperature variations, and weather systems.' },
        { name: 'Ring Systems', duration: '3 min', content: 'Explore the ring systems of Jupiter, Saturn, Uranus, and Neptune. Learn how rings form, their composition, and their dynamic nature.' },
        { name: 'Recent Discoveries', duration: '3 min', content: 'Explore recent findings from Mars rovers, Cassini mission, and New Horizons data that reshape our understanding.' }
      ],
      instructor: 'Prof. David Thompson',
      prerequisites: 'Basic astronomy knowledge'
    },
    {
      id: 4,
      title: 'Planetary Geology and Volcanism',
      category: 'Planets',
      difficulty: 'Intermediate',
      duration: '24 min',
      description: 'Study the geological processes shaping planetary surfaces.',
      rating: 4.6,
      students: 5800,
      fullDescription: 'Understand planetary geology, volcanism, plate tectonics, and how planets evolve over time.',
      lessons: ['Planetary Interiors', 'Volcanism', 'Tectonics', 'Weathering', 'Crater Formation', 'Mineral Composition'],
      instructor: 'Dr. James Lewis',
      prerequisites: 'Basic geology helpful'
    },
    // ADVANCED
    {
      id: 5,
      title: 'Exoplanet Characterization and Atmospheres',
      category: 'Planets',
      difficulty: 'Advanced',
      duration: '42 min',
      description: 'Analyze atmospheric composition and habitability of distant planets.',
      rating: 4.8,
      students: 2400,
      fullDescription: 'Advanced study of exoplanet atmospheres using spectroscopy, biosignatures, and habitability metrics.',
      lessons: ['Spectroscopy', 'Atmospheric Composition', 'Biosignatures', 'Habitability Index', 'TRAPPIST-1 Systems', 'Future Detection'],
      instructor: 'Prof. Amanda Foster',
      prerequisites: 'Advanced astronomy and physics'
    },
    {
      id: 6,
      title: 'Planetary Migration and Orbital Evolution',
      category: 'Planets',
      difficulty: 'Advanced',
      duration: '45 min',
      description: 'Study how planets move through space and gravitational interactions.',
      rating: 4.7,
      students: 1900,
      fullDescription: 'Explore planetary migration theory, resonances, and how planetary systems evolve dynamically.',
      lessons: ['N-body Problems', 'Resonances', 'Migration Theory', 'Orbital Stability', 'System Formation', 'Chaotic Dynamics'],
      instructor: 'Dr. Viktor Petrov',
      prerequisites: 'Advanced physics and mathematics'
    },
    // ===== STARS CATEGORY =====
    // BEGINNER
    {
      id: 7,
      title: 'Stars 101: Stellar Types and Classification',
      category: 'Stars',
      difficulty: 'Beginner',
      duration: '13 min',
      description: 'Learn how astronomers classify and understand different types of stars.',
      rating: 4.8,
      students: 7500,
      fullDescription: 'Introduction to stellar classification. Understand the Hertzsprung-Russell diagram and how we categorize stars.',
      lessons: [
        { name: 'Stellar Classification', duration: '2 min', content: 'Learn the spectral classification system (O, B, A, F, G, K, M) that categorizes stars by their surface temperature and composition.' },
        { name: 'HR Diagram', duration: '2 min', content: 'Understand the Hertzsprung-Russell diagram, which plots luminosity against temperature and reveals stellar properties and evolution.' },
        { name: 'Spectral Types', duration: '2 min', content: 'Explore how spectral lines reveal star composition, temperature, and rotation. Learn why absorption lines matter.' },
        { name: 'Luminosity Classes', duration: '2 min', content: 'Discover how stars are classified by size and luminosity from supergiants to white dwarfs.' },
        { name: 'Temperature Scale', duration: '2 min', content: 'Understand effective surface temperature, how it\'s measured, and its relationship to star color and spectral type.' },
        { name: 'Brightness', duration: '2 min', content: 'Learn the difference between absolute and apparent magnitude, and how astronomers measure stellar brightness.' }
      ],
      instructor: 'Dr. Aurora Wells',
      prerequisites: 'None - beginner friendly'
    },
    {
      id: 8,
      title: 'How Stars Are Born and Die',
      category: 'Stars',
      difficulty: 'Beginner',
      duration: '18 min',
      description: 'Understand the life cycle of stars from nebulae to stellar remnants.',
      rating: 4.8,
      students: 6500,
      fullDescription: 'Stars have incredible journeys. Trace stellar evolution from stellar nurseries to their final states.',
      lessons: ['Star Formation', 'Main Sequence', 'Red Giants', 'White Dwarfs', 'Neutron Stars', 'Life Cycle'],
      instructor: 'Dr. Marcus Allen',
      prerequisites: 'None - beginner level'
    },
    // INTERMEDIATE
    {
      id: 9,
      title: 'Stellar Nucleosynthesis and Energy',
      category: 'Stars',
      difficulty: 'Intermediate',
      duration: '28 min',
      description: 'Understand how stars produce energy and create elements.',
      rating: 4.7,
      students: 4200,
      fullDescription: 'Learn about nuclear fusion, the proton-proton chain, CNO cycle, and how stars forge elements.',
      lessons: ['Nuclear Fusion', 'PP Chain', 'CNO Cycle', 'Energy Transport', 'Element Creation', 'Stellar Models'],
      instructor: 'Dr. Elena Volkov',
      prerequisites: 'Basic physics knowledge'
    },
    {
      id: 10,
      title: 'Supernovae and Stellar Explosions',
      category: 'Stars',
      difficulty: 'Intermediate',
      duration: '26 min',
      description: 'Study the cataclysmic end states of massive stars.',
      rating: 4.6,
      students: 3900,
      fullDescription: 'Explore supernova types, explosion mechanics, and their role in seeding the universe with elements.',
      lessons: ['Type Ia Supernovae', 'Type II Supernovae', 'Core Collapse', 'Shockwaves', 'Element Distribution', 'Light Curves'],
      instructor: 'Prof. Michael Zhang',
      prerequisites: 'Basic astronomy'
    },
    // ADVANCED
    {
      id: 11,
      title: 'Binary Stars and Stellar Dynamics',
      category: 'Stars',
      difficulty: 'Advanced',
      duration: '38 min',
      description: 'Study complex stellar systems and binary interactions.',
      rating: 4.7,
      students: 2100,
      fullDescription: 'Explore binary star orbits, mass transfer, X-ray binaries, and how to measure stellar properties.',
      lessons: ['Orbital Mechanics', 'Mass Transfer', 'X-ray Binaries', 'Common Envelope', 'Accretion Disks', 'Observational Methods'],
      instructor: 'Prof. Nicholas Stone',
      prerequisites: 'Advanced physics required'
    },
    {
      id: 12,
      title: 'Stellar Evolution and Massive Stars',
      category: 'Stars',
      difficulty: 'Advanced',
      duration: '44 min',
      description: 'Understand detailed evolutionary tracks of all stellar types.',
      rating: 4.8,
      students: 1700,
      fullDescription: 'Advanced study of Hertzsprung-Russell tracks, evolutionary models, and the fate of massive stars.',
      lessons: ['Evolutionary Tracks', 'Mass-Luminosity', 'Wolf-Rayet Stars', 'Pulsating Variables', 'Blue Stragglers', 'Final States'],
      instructor: 'Dr. Christopher Lee',
      prerequisites: 'Advanced astrophysics'
    },
    // ===== MISSIONS CATEGORY =====
    // BEGINNER
    {
      id: 13,
      title: 'Space Exploration Milestones',
      category: 'Missions',
      difficulty: 'Beginner',
      duration: '14 min',
      description: 'Explore humanity\'s greatest achievements in space.',
      rating: 4.9,
      students: 9200,
      fullDescription: 'From Sputnik to Mars rovers, chronicle major space missions and technologies.',
      lessons: ['Space Race', 'Apollo Program', 'Space Stations', 'Telescopes', 'Rovers', 'Future Plans'],
      instructor: 'Dr. Jennifer Park',
      prerequisites: 'None - beginner friendly'
    },
    {
      id: 14,
      title: 'Spacecraft Design and Systems',
      category: 'Missions',
      difficulty: 'Beginner',
      duration: '16 min',
      description: 'Learn how spacecraft are designed and what systems keep them operational.',
      rating: 4.8,
      students: 7800,
      fullDescription: 'Understand the components, power systems, and design principles of modern spacecraft.',
      lessons: ['Structure', 'Power Systems', 'Propulsion', 'Communications', 'Thermal Control', 'Life Support'],
      instructor: 'Dr. Robert Chang',
      prerequisites: 'None - beginner level'
    },
    // INTERMEDIATE
    {
      id: 15,
      title: 'Launch Systems and Rocket Technology',
      category: 'Missions',
      difficulty: 'Intermediate',
      duration: '30 min',
      description: 'Explore how rockets are engineered to reach space.',
      rating: 4.7,
      students: 5500,
      fullDescription: 'Study rocket design, staging, engines, and the evolution of launch vehicles.',
      lessons: ['Rocket Engines', 'Staging', 'Fuel Types', 'Launch Systems', 'Reusability', 'Modern Rockets'],
      instructor: 'Prof. Lisa Martinez',
      prerequisites: 'Basic engineering knowledge'
    },
    {
      id: 16,
      title: 'Space Station Operations and Research',
      category: 'Missions',
      difficulty: 'Intermediate',
      duration: '25 min',
      description: 'Understand how space stations operate and conduct research.',
      rating: 4.6,
      students: 4700,
      fullDescription: 'Learn about ISS operations, microgravity research, and international cooperation in space.',
      lessons: ['ISS Structure', 'Microgravity Research', 'Experiments', 'Crew Operations', 'Maintenance', 'Resupply'],
      instructor: 'Dr. Anna Kowalski',
      prerequisites: 'Basic science knowledge'
    },
    // ADVANCED
    {
      id: 17,
      title: 'Advanced Rocket Science and Orbital Mechanics',
      category: 'Missions',
      difficulty: 'Advanced',
      duration: '48 min',
      description: 'Master the physics behind modern spaceflight.',
      rating: 4.5,
      students: 2300,
      fullDescription: 'Cover rocket propulsion, orbital mechanics, launch windows, and spaceflight engineering.',
      lessons: ['Rocket Equation', 'Orbital Mechanics', 'Launch Windows', 'Transfers', 'Gravity Assists', 'Reentry'],
      instructor: 'Prof. Michael Zhang',
      prerequisites: 'Physics, calculus required'
    },
    {
      id: 18,
      title: 'Deep Space Exploration and Interplanetary Travel',
      category: 'Missions',
      difficulty: 'Advanced',
      duration: '50 min',
      description: 'Understand missions beyond Earth orbit and interplanetary navigation.',
      rating: 4.7,
      students: 1900,
      fullDescription: 'Study deep space missions, navigation techniques, and challenges of exploring distant planets.',
      lessons: ['Interplanetary Trajectories', 'Navigation', 'Communication Delays', 'Solar Panels', 'RTG Power', 'Landing Systems'],
      instructor: 'Dr. James Wilson',
      prerequisites: 'Advanced aerospace engineering'
    },
    // ===== GALAXIES CATEGORY =====
    // BEGINNER
    {
      id: 19,
      title: 'Galaxy Types and Classification',
      category: 'Galaxies',
      difficulty: 'Beginner',
      duration: '15 min',
      description: 'Learn about different types of galaxies in the universe.',
      rating: 4.8,
      students: 8200,
      fullDescription: 'Understand Hubble\'s galaxy classification, spiral galaxies, elliptical galaxies, and irregular forms.',
      lessons: ['Classification System', 'Spiral Galaxies', 'Elliptical Galaxies', 'Irregular Forms', 'Active Galaxies', 'Examples'],
      instructor: 'Dr. Kevin Brown',
      prerequisites: 'None - beginner friendly'
    },
    {
      id: 20,
      title: 'Types of Galaxies and the Milky Way',
      category: 'Galaxies',
      difficulty: 'Beginner',
      duration: '16 min',
      description: 'Learn about galaxy types and our place in the Milky Way.',
      rating: 4.8,
      students: 7800,
      fullDescription: 'Discover galaxy structure and our galactic environment within the Milky Way.',
      lessons: ['Galaxy Classification', 'Spiral Structure', 'Galactic Center', 'Milky Way Structure', 'Our Position', 'Rotation'],
      instructor: 'Dr. Jennifer Park',
      prerequisites: 'None - beginner level'
    },
    // INTERMEDIATE
    {
      id: 21,
      title: 'Galactic Structure and Dynamics',
      category: 'Galaxies',
      difficulty: 'Intermediate',
      duration: '29 min',
      description: 'Study how galaxies are structured and how they move.',
      rating: 4.6,
      students: 4500,
      fullDescription: 'Explore galactic rotation curves, disk structure, bulges, and gravitational dynamics.',
      lessons: ['Rotation Curves', 'Disk Structure', 'Bulges', 'Halos', 'Density Waves', 'Star Formation'],
      instructor: 'Prof. Daniel Foster',
      prerequisites: 'Basic astronomy'
    },
    {
      id: 22,
      title: 'Galaxy Collisions and Mergers',
      category: 'Galaxies',
      difficulty: 'Intermediate',
      duration: '27 min',
      description: 'Understand what happens when galaxies collide.',
      rating: 4.7,
      students: 3800,
      fullDescription: 'Study galaxy interactions, mergers, and how they reshape galactic structures.',
      lessons: ['Collision Dynamics', 'Merger Types', 'Tidal Effects', 'Starburst Galaxies', 'Examples', 'Andromeda Future'],
      instructor: 'Dr. Susan Hayes',
      prerequisites: 'Basic physics knowledge'
    },
    // ADVANCED
    {
      id: 23,
      title: 'Dark Matter and Galactic Dynamics',
      category: 'Galaxies',
      difficulty: 'Advanced',
      duration: '41 min',
      description: 'Investigate dark matter that dominates galaxies.',
      rating: 4.6,
      students: 1800,
      fullDescription: 'Explore evidence for dark matter, detection methods, and its role in galaxy formation.',
      lessons: ['Rotation Curves', 'Dark Matter Evidence', 'Candidates', 'Detection', 'Galaxy Clusters', 'Formation'],
      instructor: 'Prof. Elena Volkov',
      prerequisites: 'Advanced astrophysics'
    },
    {
      id: 24,
      title: 'Active Galactic Nuclei and Supermassive Black Holes',
      category: 'Galaxies',
      difficulty: 'Advanced',
      duration: '46 min',
      description: 'Study the powerful cores of active galaxies.',
      rating: 4.8,
      students: 2200,
      fullDescription: 'Understand AGN, jets, accretion disks, and supermassive black holes at galaxy centers.',
      lessons: ['AGN Types', 'Supermassive Black Holes', 'Accretion Disks', 'Jets and Lobes', 'Quasars', 'Unified Model'],
      instructor: 'Dr. Thomas Anderson',
      prerequisites: 'Advanced astrophysics required'
    },
    // ===== ASTRONOMY CATEGORY =====
    // BEGINNER
    {
      id: 25,
      title: 'Introduction to Constellations',
      category: 'Astronomy',
      difficulty: 'Beginner',
      duration: '12 min',
      description: 'Learn to identify constellations and navigate the night sky.',
      rating: 4.7,
      students: 6200,
      fullDescription: 'Explore the stories behind constellations and how to find them in the night sky.',
      lessons: ['What are Constellations?', 'Ancient Maps', 'Northern Hemisphere', 'Southern Hemisphere', 'Star Charts', 'Best Times'],
      instructor: 'Dr. Marcus Allen',
      prerequisites: 'None - perfect for beginners'
    },
    {
      id: 26,
      title: 'Observational Astronomy for Beginners',
      category: 'Astronomy',
      difficulty: 'Beginner',
      duration: '14 min',
      description: 'Learn how to observe the night sky with your eyes and binoculars.',
      rating: 4.8,
      students: 7400,
      fullDescription: 'Practical guide to stargazing, identifying bright stars, planets, and deep-sky objects.',
      lessons: ['Eye Adaptation', 'Star Brightness', 'Apparent Motion', 'Binoculars', 'Best Viewing', 'Seasonal Objects'],
      instructor: 'Dr. Patricia Wells',
      prerequisites: 'None - beginner level'
    },
    // INTERMEDIATE
    {
      id: 27,
      title: 'Understanding Black Holes',
      category: 'Astronomy',
      difficulty: 'Intermediate',
      duration: '25 min',
      description: 'Learn about the mysterious objects that shape spacetime.',
      rating: 4.8,
      students: 5200,
      fullDescription: 'Comprehensive course on black hole physics, event horizons, singularities, and observations.',
      lessons: ['What is a Black Hole?', 'Formation', 'Event Horizons', 'Spacetime', 'Observing', 'Galaxies'],
      instructor: 'Dr. Sarah Chen',
      prerequisites: 'Basic gravity knowledge'
    },
    {
      id: 28,
      title: 'Neutron Stars and Pulsars',
      category: 'Astronomy',
      difficulty: 'Intermediate',
      duration: '23 min',
      description: 'Study the incredibly dense remnants of massive stars.',
      rating: 4.6,
      students: 4100,
      fullDescription: 'Learn about neutron star formation, properties, pulsars, and pulsar timing.',
      lessons: ['Formation', 'Extreme Density', 'Neutron Degenerate Matter', 'Pulsars', 'Timing', 'Pulsar Planets'],
      instructor: 'Dr. Richard Hayes',
      prerequisites: 'Basic astronomy'
    },
    // ADVANCED
    {
      id: 29,
      title: 'Quantum Mechanics in Astrophysics',
      category: 'Astronomy',
      difficulty: 'Advanced',
      duration: '52 min',
      description: 'Master quantum principles in astrophysical phenomena.',
      rating: 4.9,
      students: 2900,
      fullDescription: 'Explore quantum mechanics in stellar nucleosynthesis, particle interactions, and dark matter implications.',
      lessons: ['Quantum Foundations', 'Tunneling', 'Degenerate Matter', 'Neutron Stars', 'Quantum Effects', 'Dark Matter'],
      instructor: 'Dr. Viktor Petrov',
      prerequisites: 'Advanced physics required'
    },
    {
      id: 30,
      title: 'High-Energy Astrophysics and Gamma-Ray Bursts',
      category: 'Astronomy',
      difficulty: 'Advanced',
      duration: '48 min',
      description: 'Study extreme cosmic phenomena at the highest energies.',
      rating: 4.7,
      students: 1800,
      fullDescription: 'Understand gamma-ray bursts, X-ray binaries, cosmic rays, and extreme astrophysics.',
      lessons: ['X-ray Astronomy', 'Gamma-ray Bursts', 'Cosmic Rays', 'Accretion', 'Relativistic Jets', 'Detection'],
      instructor: 'Prof. Alexandra Novak',
      prerequisites: 'Advanced astrophysics'
    },
    // ===== COSMOLOGY CATEGORY =====
    // BEGINNER
    {
      id: 31,
      title: 'Introduction to Cosmology',
      category: 'Cosmology',
      difficulty: 'Beginner',
      duration: '13 min',
      description: 'Learn about the universe\'s origin, expansion, and fate.',
      rating: 4.8,
      students: 8600,
      fullDescription: 'Beginner-friendly introduction to the universe. Understand cosmology basics and fundamental concepts.',
      lessons: ['Universe Scale', 'Expansion', 'Observable Universe', 'Cosmic History', 'Big Bang Basics', 'Future of Universe'],
      instructor: 'Dr. Walter Stone',
      prerequisites: 'None - beginner friendly'
    },
    {
      id: 32,
      title: 'The Solar Wind and Space Weather',
      category: 'Cosmology',
      difficulty: 'Beginner',
      duration: '17 min',
      description: 'Understand how the Sun influences space around us.',
      rating: 4.7,
      students: 6800,
      fullDescription: 'Learn about solar wind, space weather, and how it affects Earth and technology.',
      lessons: ['Solar Wind Basics', 'Solar Flares', 'CME', 'Magnetosphere', 'Aurora', 'Space Weather'],
      instructor: 'Dr. Linda Gray',
      prerequisites: 'None - beginner level'
    },
    // INTERMEDIATE
    {
      id: 33,
      title: 'Cosmic Microwave Background and Early Universe',
      category: 'Cosmology',
      difficulty: 'Intermediate',
      duration: '28 min',
      description: 'Study the universe\'s oldest light and what it tells us.',
      rating: 4.6,
      students: 4200,
      fullDescription: 'Learn about the CMB, its origin, anisotropies, and what it reveals about early universe.',
      lessons: ['Early Universe', 'Recombination', 'CMB Discovery', 'Anisotropies', 'Polarization', 'Implications'],
      instructor: 'Prof. Geoffrey White',
      prerequisites: 'Basic cosmology'
    },
    {
      id: 34,
      title: 'Dark Energy and Cosmic Acceleration',
      category: 'Cosmology',
      difficulty: 'Intermediate',
      duration: '26 min',
      description: 'Explore the mysterious force accelerating the universe\'s expansion.',
      rating: 4.7,
      students: 3600,
      fullDescription: 'Understand dark energy, type Ia supernovae, the cosmological constant, and acceleration.',
      lessons: ['Universe Expansion', 'Acceleration Discovery', 'Dark Energy', 'Cosmological Constant', 'Quintessence', 'Fate'],
      instructor: 'Dr. Helena Marks',
      prerequisites: 'Basic cosmology'
    },
    // ADVANCED
    {
      id: 35,
      title: 'The Big Bang Theory',
      category: 'Cosmology',
      difficulty: 'Advanced',
      duration: '45 min',
      description: 'Explore the universe\'s origins and supporting evidence.',
      rating: 4.6,
      students: 3800,
      fullDescription: 'Dive deep into cosmology covering inflation, nucleosynthesis, and cosmic microwave background.',
      lessons: ['Beginning of Time', 'Cosmic Inflation', 'Early Physics', 'Nucleosynthesis', 'CMB', 'Evidence'],
      instructor: 'Prof. James Wilson',
      prerequisites: 'Advanced physics'
    },
    {
      id: 36,
      title: 'Inflation Theory and Cosmological Parameters',
      category: 'Cosmology',
      difficulty: 'Advanced',
      duration: '50 min',
      description: 'Understand modern cosmic inflation and universe parameters.',
      rating: 4.8,
      students: 2100,
      fullDescription: 'Advanced study of inflation theory, primordial fluctuations, and precise cosmological measurements.',
      lessons: ['Inflation Mechanism', 'Quantum Fluctuations', 'Flatness Problem', 'Hubble Parameter', 'Density Parameters', 'Observational Tests'],
      instructor: 'Dr. Yuki Tanaka',
      prerequisites: 'Advanced physics and mathematics'
    }
  ];

  // Filter mock data based on selected category and difficulty
  const getFilteredContent = () => {
    const baseContent = content.length > 0 ? content : mockContent;
    
    return baseContent.filter(item => {
      const categoryMatch = !category || item.category.toLowerCase() === category.toLowerCase();
      const difficultyMatch = !difficulty || item.difficulty.toLowerCase() === difficulty.toLowerCase();
      return categoryMatch && difficultyMatch;
    });
  };

  const displayContent = getFilteredContent();

  const getDifficultyColor = (diff) => {
    switch (diff?.toLowerCase()) {
      case 'beginner':
        return 'from-green-500/20 to-emerald-500/10 border-green-500/40';
      case 'intermediate':
        return 'from-yellow-500/20 to-orange-500/10 border-yellow-500/40';
      case 'advanced':
        return 'from-red-500/20 to-pink-500/10 border-red-500/40';
      default:
        return 'from-indigo-500/20 to-purple-500/10 border-indigo-500/40';
    }
  };

  const getDifficultyBadge = (diff) => {
    switch (diff?.toLowerCase()) {
      case 'beginner':
        return 'bg-green-500/30 text-green-300';
      case 'intermediate':
        return 'bg-yellow-500/30 text-yellow-300';
      case 'advanced':
        return 'bg-red-500/30 text-red-300';
      default:
        return 'bg-indigo-500/30 text-indigo-300';
    }
  };

  return (
    <div className="space-y-8">
      {/* Header */}
      <div className="text-center py-8">
        <h1 className="text-5xl font-bold neon mb-2 flex items-center justify-center gap-3">
          <FaBook className="text-purple-400" />
          Learning Zone
        </h1>
        <p className="text-gray-300 text-lg glow-text">Educational resources about space exploration and astronomy</p>
        <div className="mt-4 h-1 w-32 mx-auto bg-gradient-to-r from-purple-500 via-pink-500 to-purple-500 rounded-full"></div>
      </div>

      {/* Learning Stats */}
      <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
        <div className="glass-card space-card glow-border text-center p-4">
          <p className="text-cyan-400 text-2xl font-bold">{displayContent.length}</p>
          <p className="text-gray-300 text-sm mt-1">Courses</p>
        </div>
        <div className="glass-card space-card glow-border text-center p-4">
          <p className="text-cyan-400 text-2xl font-bold">25+</p>
          <p className="text-gray-300 text-sm mt-1">Hours</p>
        </div>
        <div className="glass-card space-card glow-border text-center p-4">
          <p className="text-cyan-400 text-2xl font-bold">15k+</p>
          <p className="text-gray-300 text-sm mt-1">Learners</p>
        </div>
        <div className="glass-card space-card glow-border text-center p-4">
          <p className="text-cyan-400 text-2xl font-bold">📚</p>
          <p className="text-gray-300 text-sm mt-1">Resources</p>
        </div>
      </div>

      {/* Filters */}
      <div className="glass-card space-card glow-border p-6">
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div>
            <label className="text-cyan-300 text-sm font-semibold block mb-3">Category</label>
            <select
              value={category || ''}
              onChange={(e) => setCategory(e.target.value || null)}
              className="w-full px-4 py-3 bg-indigo-900/30 text-white rounded-lg border border-indigo-500/30 focus:border-indigo-500/60 focus:outline-none transition neon-btn"
            >
              <option value="">All Categories</option>
              <option value="planets">Planets</option>
              <option value="stars">Stars</option>
              <option value="galaxies">Galaxies</option>
              <option value="missions">Missions</option>
              <option value="astronomy">Astronomy</option>
              <option value="cosmology">Cosmology</option>
            </select>
          </div>
          <div>
            <label className="text-cyan-300 text-sm font-semibold block mb-3">Difficulty</label>
            <select
              value={difficulty || ''}
              onChange={(e) => setDifficulty(e.target.value || null)}
              className="w-full px-4 py-3 bg-indigo-900/30 text-white rounded-lg border border-indigo-500/30 focus:border-indigo-500/60 focus:outline-none transition neon-btn"
            >
              <option value="">All Levels</option>
              <option value="beginner">Beginner</option>
              <option value="intermediate">Intermediate</option>
              <option value="advanced">Advanced</option>
            </select>
          </div>
        </div>
      </div>

      {loading && <div className="text-center text-cyan-400 py-8 text-lg">🔄 Loading courses...</div>}
      {error && <div className="text-center text-red-400 py-8 text-lg">⚠️ {error}</div>}

      {/* Course Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        {displayContent.map((item, idx) => (
          <div
            key={idx}
            className={`glass-card space-card glow-border border bg-gradient-to-br ${getDifficultyColor(item.difficulty)}`}
          >
            {/* Header */}
            <div className="mb-4 pb-4 border-b border-white/10">
              <div className="flex items-start justify-between mb-3">
                <h3 className="text-xl font-bold neon flex-1">{item.title}</h3>
                <FaBook className="text-purple-400 text-lg mt-1" />
              </div>
              <p className="text-gray-300 text-sm leading-relaxed">{item.description}</p>
            </div>

            {/* Course Info */}
            <div className="space-y-3 mb-4">
              <div className="flex items-center justify-between text-sm">
                <span className={`px-3 py-1 rounded-full font-semibold text-xs ${getDifficultyBadge(item.difficulty)}`}>
                  {item.difficulty}
                </span>
                <span className="text-gray-400 text-xs">⏱️ {item.duration || '20 min'}</span>
              </div>

              <div className="bg-white/5 rounded-lg p-3 border border-white/10">
                <div className="flex items-center justify-between mb-2">
                  <span className="text-white/70 text-xs">COURSE RATING</span>
                  <span className="text-yellow-300 font-bold">{item.rating || 4.7}★</span>
                </div>
                <div className="flex gap-1">
                  {[...Array(5)].map((_, i) => (
                    <FaStar
                      key={i}
                      className={`text-xs ${i < Math.floor(item.rating || 4.7) ? 'text-yellow-400' : 'text-white/20'}`}
                    />
                  ))}
                </div>
              </div>

              <div className="bg-white/5 rounded-lg p-3 border border-white/10">
                <p className="text-white/70 text-xs mb-1">STUDENTS ENROLLED</p>
                <p className="text-cyan-300 font-bold">{item.students || 5000}+</p>
              </div>
            </div>

            {/* Action Button */}
            <button 
              onClick={() => setSelectedCourse(item)}
              className="w-full neon-btn flex items-center justify-center gap-2"
            >
              <FaPlayCircle /> Start Learning
            </button>
          </div>
        ))}
      </div>

      {/* Detail Modal */}
      <DetailModal
        isOpen={!!selectedCourse}
        title={selectedCourse?.title}
        onClose={() => setSelectedCourse(null)}
      >
        {selectedCourse && (
          <div className="space-y-4">
            <p className="text-gray-100 leading-relaxed">{selectedCourse.fullDescription}</p>

            <div className="bg-indigo-900/30 border border-indigo-500/30 rounded-lg p-4">
              <h3 className="text-cyan-300 font-bold mb-3">📊 Course Info</h3>
              <div className="grid grid-cols-2 gap-3 text-sm">
                <div>
                  <p className="text-gray-400">Instructor</p>
                  <p className="text-white font-semibold">{selectedCourse.instructor}</p>
                </div>
                <div>
                  <p className="text-gray-400">Duration</p>
                  <p className="text-white font-semibold">{selectedCourse.duration}</p>
                </div>
                <div>
                  <p className="text-gray-400">Students</p>
                  <p className="text-white font-semibold">{selectedCourse.students}+</p>
                </div>
                <div>
                  <p className="text-gray-400">Rating</p>
                  <p className="text-white font-semibold">{selectedCourse.rating}★</p>
                </div>
              </div>
            </div>

            {selectedCourse.prerequisites && (
              <div className="bg-orange-900/30 border border-orange-500/30 rounded-lg p-4">
                <h3 className="text-orange-300 font-bold mb-2">📋 Prerequisites</h3>
                <p className="text-gray-100 text-sm">{selectedCourse.prerequisites}</p>
              </div>
            )}

            {selectedCourse.lessons && (
              <div className="bg-purple-900/30 border border-purple-500/30 rounded-lg p-4">
                <h3 className="text-purple-300 font-bold mb-3">📚 Lessons Included</h3>
                <ul className="space-y-2">
                  {selectedCourse.lessons.map((lesson, idx) => {
                    const lessonData = typeof lesson === 'string' ? { name: lesson } : lesson;
                    return (
                      <li
                        key={idx}
                        onClick={() => setSelectedLesson(lessonData)}
                        className="flex items-start gap-2 text-sm cursor-pointer hover:bg-purple-500/20 p-2 rounded transition"
                      >
                        <span className="text-purple-400 mt-1">📖</span>
                        <div className="flex-1">
                          <span className="text-gray-100 font-semibold block">{lessonData.name}</span>
                          {lessonData.duration && <span className="text-gray-400 text-xs">{lessonData.duration}</span>}
                        </div>
                        {lessonData.content && <span className="text-cyan-400 text-xs">Click to learn</span>}
                      </li>
                    );
                  })}
                </ul>
              </div>
            )}

            <button
              onClick={() => {
                alert(`🎓 Starting course: ${selectedCourse.title}!\n\nLessons loading...`);
                setSelectedCourse(null);
              }}
              className="w-full bg-gradient-to-r from-indigo-600 to-purple-600 hover:from-indigo-700 hover:to-purple-700 text-white px-4 py-3 rounded-lg font-semibold transition mt-4"
            >
              <FaPlayCircle className="inline mr-2" /> Start Learning Now
            </button>
          </div>
        )}
      </DetailModal>

      {!loading && displayContent.length === 0 && (
        <div className="text-center py-12">
          <p className="text-gray-400 text-xl">No content found</p>
        </div>
      )}

      {/* Lesson Detail Modal */}
      <LessonModal
        isOpen={!!selectedLesson}
        lesson={selectedLesson}
        onClose={() => setSelectedLesson(null)}
      />
    </div>
  );
}

export default LearningZone;
