import React, { useState, useEffect } from 'react';
import { api } from '../utils/api';
import { 
  HomeIcon, 
  BuildingOfficeIcon, 
  CurrencyDollarIcon,
  TrendingUpIcon,
  CheckCircleIcon
} from '@heroicons/react/24/outline';

const Dashboard = () => {
  const [stats, setStats] = useState({
    totalProperties: 0,
    averagePrice: 0,
    marketGrowth: 0,
    activeCities: 0
  });
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchDashboardStats = async () => {
      try {
        setLoading(true);
        const response = await api.get('/analytics/overview');
        setStats({
          totalProperties: response.total_properties,
          averagePrice: response.average_price_tzs,
          marketGrowth: 12.5, // Sample growth rate
          activeCities: response.total_cities_covered
        });
        setLoading(false);
      } catch (err) {
        setError('Failed to load dashboard statistics');
        setLoading(false);
      }
    };

    fetchDashboardStats();
  }, []);

  const formatCurrency = (amount) => {
    return new Intl.NumberFormat('en-TZ', {
      style: 'currency',
      currency: 'TZS',
      minimumFractionDigits: 0,
      maximumFractionDigits: 0,
    }).format(amount);
  };

  const statCards = [
    {
      title: 'Total Properties',
      value: stats.totalProperties,
      icon: BuildingOfficeIcon,
      color: 'bg-blue-500',
      change: '+12%',
      changeType: 'increase'
    },
    {
      title: 'Average Price',
      value: formatCurrency(stats.averagePrice),
      icon: CurrencyDollarIcon,
      color: 'bg-green-500',
      change: '+8%',
      changeType: 'increase'
    },
    {
      title: 'Market Growth',
      value: `${stats.marketGrowth}%`,
      icon: TrendingUpIcon,
      color: 'bg-purple-500',
      change: '+2.3%',
      changeType: 'increase'
    },
    {
      title: 'Active Cities',
      value: stats.activeCities,
      icon: HomeIcon,
      color: 'bg-orange-500',
      change: '+2',
      changeType: 'increase'
    }
  ];

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-500"></div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="text-center py-12">
        <div className="text-red-500 text-6xl mb-4">⚠️</div>
        <h3 className="text-lg font-medium text-gray-900">Error Loading Dashboard</h3>
        <p className="mt-2 text-gray-600">{error}</p>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="bg-white overflow-hidden shadow rounded-lg">
        <div className="p-6">
          <div className="flex items-center">
            <div className="flex-shrink-0">
              <div className="text-3xl font-bold text-blue-600">🏠</div>
              <div className="ml-4 text-2xl font-semibold text-gray-900">
                Dashboard
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Stats Grid */}
      <div className="grid grid-cols-1 gap-6 sm:grid-cols-2 lg:grid-cols-4">
        {statCards.map((stat, index) => (
          <div key={index} className="bg-white overflow-hidden shadow rounded-lg">
            <div className="p-5">
              <div className="flex items-center">
                <div className={`flex-shrink-0 p-3 rounded-md ${stat.color}`}>
                  <stat.icon className="h-6 w-6 text-white" aria-hidden="true" />
                </div>
                <div className="ml-5 w-0 flex-1">
                  <dl>
                    <dt className="text-sm font-medium text-gray-500 truncate">{stat.title}</dt>
                    <dd className="flex items-baseline">
                      <div className="text-2xl font-semibold text-gray-900">{stat.value}</div>
                      {stat.change && (
                        <div className={`ml-2 flex items-baseline text-sm font-semibold ${
                          stat.changeType === 'increase' ? 'text-green-600' : 'text-red-600'
                        }`}>
                          <span>{stat.change}</span>
                          <CheckCircleIcon className="h-4 w-4 ml-1" aria-hidden="true" />
                        </div>
                      )}
                    </dd>
                  </dl>
                </div>
              </div>
            </div>
          </div>
        ))}
      </div>

      {/* Quick Actions */}
      <div className="bg-white shadow rounded-lg">
        <div className="px-6 py-4">
          <h3 className="text-lg font-medium text-gray-900 mb-4">Quick Actions</h3>
          <div className="grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-3">
            <button
              onClick={() => window.location.href = '/properties'}
              className="relative block w-full p-3 border-2 border-gray-300 rounded-lg bg-white text-sm font-medium text-gray-700 hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
            >
              <span className="absolute inset-y-0 left-0 flex items-center pl-3">
                <BuildingOfficeIcon className="h-5 w-5 text-gray-400" aria-hidden="true" />
              </span>
              Browse Properties
            </button>
            <button
              onClick={() => window.location.href = '/predictions'}
              className="relative block w-full p-3 border-2 border-gray-300 rounded-lg bg-white text-sm font-medium text-gray-700 hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
            >
              <span className="absolute inset-y-0 left-0 flex items-center pl-3">
                <CurrencyDollarIcon className="h-5 w-5 text-gray-400" aria-hidden="true" />
              </span>
              Predict Price
            </button>
            <button
              onClick={() => window.location.href = '/analytics'}
              className="relative block w-full p-3 border-2 border-gray-300 rounded-lg bg-white text-sm font-medium text-gray-700 hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
            >
              <span className="absolute inset-y-0 left-0 flex items-center pl-3">
                <TrendingUpIcon className="h-5 w-5 text-gray-400" aria-hidden="true" />
              </span>
              View Analytics
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Dashboard;
