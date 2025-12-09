<script>
  import Icon from '@iconify/svelte';
  import { motionInView, motionHover } from '../utils/motion.js';
  import { createDateRangePicker, melt } from '@melt-ui/svelte';
  import AnalyticsChart from '../components/AnalyticsChart.svelte';
  import { _ } from 'svelte-i18n';
  import { 
    exportAnalyticsData, 
    exportOverviewData, 
    exportTopProductsData, 
    exportRecentActivityData 
  } from '../utils/export.js';

  // State variables for Skyplot inputs
  let targetsInput = "";
  let startTimeInput = "";

  // Function to handle Skyplot updates
  function updateSkyplot() {
    console.log("Updating Skyplot with targets:", targetsInput, "and start time:", startTimeInput);
    // Add logic to update the Skyplot image dynamically if needed
  }

  // Analytics data
  let analyticsData = {
    overview: {
      totalRevenue: '$125,430',
      totalUsers: '45,231',
      conversionRate: '3.24%',
      avgSessionDuration: '2m 34s'
    },
    trends: [
      { month: 'Jan', revenue: 12000, users: 8500, conversions: 320 },
      { month: 'Feb', revenue: 15000, users: 9200, conversions: 380 },
      { month: 'Mar', revenue: 18000, users: 10500, conversions: 420 },
      { month: 'Apr', revenue: 22000, users: 11800, conversions: 480 },
      { month: 'May', revenue: 25000, users: 13200, conversions: 520 },
      { month: 'Jun', revenue: 28000, users: 14500, conversions: 580 }
    ],
    topProducts: [
      { name: $_("analytics.premium_plan"), sales: 1240, revenue: '$45,200' },
      { name: $_("analytics.basic_plan"), sales: 890, revenue: '$22,300' },
      { name: $_("analytics.enterprise"), sales: 320, revenue: '$58,900' }
    ],
    recentActivity: [
      { action: $_("analytics.new_user_registered"), time: '2 ' + $_("analytics.min_ago"), type: 'user' },
      { action: $_("analytics.payment_received"), time: '5 ' + $_("analytics.min_ago"), type: 'payment' },
      { action: $_("analytics.product_purchased"), time: '8 ' + $_("analytics.min_ago"), type: 'purchase' },
      { action: $_("analytics.support_ticket"), time: '12 ' + $_("analytics.min_ago"), type: 'support' }
    ]
  };
  
  let selectedPeriod = '30d';
  let selectedMetric = 'revenue';
  let showMetricSelect = false;
  let showExportMenu = false;
  
  // Icon background colors for different stat types
  const iconColors = {
    'heroicons:currency-dollar': 'from-emerald-500 to-teal-600',
    'heroicons:users': 'from-blue-500 to-indigo-600',
    'heroicons:chart-bar': 'from-purple-500 to-pink-600',
    'heroicons:clock': 'from-orange-500 to-red-600',
    'heroicons:calendar': 'from-red-500 to-pink-600',
    'heroicons:arrow-down-tray': 'from-green-500 to-emerald-600',
    'heroicons:chevron-down': 'from-gray-500 to-slate-600',
    'heroicons:chevron-up': 'from-green-500 to-emerald-600',
    'heroicons:chevron-left': 'from-blue-500 to-indigo-600',
    'heroicons:chevron-right': 'from-blue-500 to-indigo-600',
    'heroicons:eye': 'from-blue-500 to-indigo-600',
    'heroicons:arrow-uturn-left': 'from-red-500 to-pink-600',
    'heroicons:banknotes': 'from-green-500 to-emerald-600',
    'heroicons:user-circle': 'from-purple-500 to-pink-600',
    'heroicons:user': 'from-blue-500 to-indigo-600',
    'heroicons:credit-card': 'from-green-500 to-emerald-600',
    'heroicons:shopping-cart': 'from-orange-500 to-red-600',
    'heroicons:chat-bubble-left-right': 'from-purple-500 to-pink-600',
    'heroicons:ellipsis-horizontal': 'from-gray-500 to-slate-600',
    'heroicons:arrow-path': 'from-blue-500 to-indigo-600',
    'heroicons:arrow-trending-up': 'from-green-500 to-emerald-600',
    'heroicons:arrow-trending-down': 'from-red-500 to-pink-600',
    'heroicons:presentation-chart-line': 'from-purple-500 to-pink-600',
    'heroicons:cube': 'from-orange-500 to-red-600',
    'heroicons:document-arrow-down': 'from-teal-500 to-cyan-600'
  };
  
  const metricOptions = [
    { value: 'revenue', label: $_("analytics.revenue") },
    { value: 'users', label: $_("analytics.users") },
    { value: 'conversions', label: $_("analytics.conversions") },
    { value: 'engagement', label: $_("analytics.engagement") }
  ];
  
  // Melt UI Date Range Picker
  const {
    elements: {
      calendar,
      cell,
      content,
      field,
      grid,
      heading,
      label,
      nextButton,
      prevButton,
      startSegment,
      endSegment,
      trigger
    },
    states: { months, headingValue, weekdays, segmentContents },
    helpers: { isDateDisabled, isDateUnavailable }
  } = createDateRangePicker();
  
  // Subscribe to stores at the top level to avoid scoped subscription errors
  $: weekdaysArray = $weekdays;
  $: monthsArray = $months;
  $: headingValueText = $headingValue;
  $: segmentContentsData = $segmentContents;
  $: isDateDisabledFn = $isDateDisabled;
  $: isDateUnavailableFn = $isDateUnavailable;
  
  function toggleMetricSelect() {
    showMetricSelect = !showMetricSelect;
  }
  
  function selectMetric(value) {
    selectedMetric = value;
    showMetricSelect = false;
  }

  function toggleExportMenu() {
    showExportMenu = !showExportMenu;
  }

  function exportData(type) {
    switch (type) {
      case 'chart':
        exportAnalyticsData(analyticsData, selectedMetric, 'monthly');
        break;
      case 'overview':
        exportOverviewData(analyticsData.overview);
        break;
      case 'products':
        exportTopProductsData(analyticsData.topProducts);
        break;
      case 'activity':
        exportRecentActivityData(analyticsData.recentActivity);
        break;
      case 'all':
        // Export all data
        exportAnalyticsData(analyticsData, selectedMetric, 'monthly');
        setTimeout(() => exportOverviewData(analyticsData.overview), 100);
        setTimeout(() => exportTopProductsData(analyticsData.topProducts), 200);
        setTimeout(() => exportRecentActivityData(analyticsData.recentActivity), 300);
        break;
    }
    showExportMenu = false;
  }

  // Close menus when clicking outside
  function handleClickOutside(event) {
    if (showMetricSelect && !event.target.closest('.metric-selector')) {
      showMetricSelect = false;
    }
    if (showExportMenu && !event.target.closest('.export-menu')) {
      showExportMenu = false;
    }
  }
</script>

<div class="space-y-8">
  <!-- Page header with enhanced styling -->
  <div class="relative overflow-hidden bg-gradient-to-r from-primary/5 via-secondary/5 to-accent/5 rounded-2xl p-6 border border-base-300/50" use:motionInView={{ animation: 'fadeInDown' }}>
    <!-- Background decorative elements -->
    <div class="absolute top-0 right-0 w-16 h-16 opacity-10">
      <Icon icon="heroicons:chart-bar" class="w-full h-full text-primary" />
    </div>
    <div class="absolute bottom-0 left-0 w-24 h-24 opacity-10">
      <Icon icon="heroicons:presentation-chart-line" class="w-full h-full text-secondary" />
    </div>
    
    <div class="relative flex items-center justify-between">
      <div>
        <h1 class="text-3xl font-bold text-primary">{$_("analytics.title")}</h1>
        <p class="mt-2 text-sm text-base-content/70 max-w-md">{$_("analytics.description")}</p>
      </div>
      <div class="flex items-center space-x-4">
      </div>
    </div>
  </div>
  
  <!-- Enhanced Analytics Overview Cards -->
  <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6" use:motionInView={{ animation: 'fadeInUp' }}>
    <div class="group relative overflow-hidden bg-gradient-to-br from-base-100 to-base-200/30 rounded-2xl shadow-md border border-base-300/50 p-5 hover:shadow-lg hover:scale-105 transition-all duration-300 backdrop-blur-sm" use:motionHover>
      <!-- Background decoration -->
      <div class="absolute top-0 right-0 w-16 h-16 opacity-5 group-hover:opacity-10 transition-opacity duration-300">
        <Icon icon="heroicons:currency-dollar" class="w-full h-full text-primary" />
      </div>
      
      <!-- Glow effect -->
      <div class="absolute inset-0 bg-gradient-to-r from-primary/5 to-secondary/5 opacity-0 group-hover:opacity-100 transition-opacity duration-300 rounded-2xl"></div>
      
      <div class="relative flex items-center justify-between">
        <div>
          <p class="text-sm font-medium text-base-content/70">{$_("analytics.total_revenue")}</p>
          <p class="text-2xl font-bold text-base-content group-hover:text-primary transition-colors duration-300">{analyticsData.overview.totalRevenue}</p>
          <p class="text-sm text-success">+12.5% {$_("analytics.from_last_month")}</p>
        </div>
        <div class="w-12 h-12 bg-gradient-to-br {iconColors['heroicons:currency-dollar']} rounded-xl flex items-center justify-center shadow-md group-hover:shadow-lg transition-shadow duration-300">
          <Icon icon="heroicons:currency-dollar" class="w-6 h-6 text-white group-hover:scale-110 transition-transform duration-300" />
        </div>
      </div>
    </div>
    
    <div class="group relative overflow-hidden bg-gradient-to-br from-base-100 to-base-200/30 rounded-2xl shadow-md border border-base-300/50 p-5 hover:shadow-lg hover:scale-105 transition-all duration-300 backdrop-blur-sm" use:motionHover>
      <!-- Background decoration -->
      <div class="absolute top-0 right-0 w-16 h-16 opacity-5 group-hover:opacity-10 transition-opacity duration-300">
        <Icon icon="heroicons:users" class="w-full h-full text-primary" />
      </div>
      
      <!-- Glow effect -->
      <div class="absolute inset-0 bg-gradient-to-r from-primary/5 to-secondary/5 opacity-0 group-hover:opacity-100 transition-opacity duration-300 rounded-2xl"></div>
      
      <div class="relative flex items-center justify-between">
        <div>
          <p class="text-sm font-medium text-base-content/70">{$_("analytics.total_users")}</p>
          <p class="text-2xl font-bold text-base-content group-hover:text-primary transition-colors duration-300">{analyticsData.overview.totalUsers}</p>
          <p class="text-sm text-success">+8.2% {$_("analytics.from_last_month")}</p>
        </div>
        <div class="w-12 h-12 bg-gradient-to-br {iconColors['heroicons:users']} rounded-xl flex items-center justify-center shadow-md group-hover:shadow-lg transition-shadow duration-300">
          <Icon icon="heroicons:users" class="w-6 h-6 text-white group-hover:scale-110 transition-transform duration-300" />
        </div>
      </div>
    </div>
    
    <div class="group relative overflow-hidden bg-gradient-to-br from-base-100 to-base-200/30 rounded-2xl shadow-md border border-base-300/50 p-5 hover:shadow-lg hover:scale-105 transition-all duration-300 backdrop-blur-sm" use:motionHover>
      <!-- Background decoration -->
      <div class="absolute top-0 right-0 w-16 h-16 opacity-5 group-hover:opacity-10 transition-opacity duration-300">
        <Icon icon="heroicons:chart-bar" class="w-full h-full text-secondary" />
      </div>
      
      <!-- Glow effect -->
      <div class="absolute inset-0 bg-gradient-to-r from-primary/5 to-secondary/5 opacity-0 group-hover:opacity-100 transition-opacity duration-300 rounded-2xl"></div>
      
      <div class="relative flex items-center justify-between">
        <div>
          <p class="text-sm font-medium text-base-content/70">{$_("analytics.conversion_rate")}</p>
          <p class="text-2xl font-bold text-base-content group-hover:text-primary transition-colors duration-300">{analyticsData.overview.conversionRate}</p>
          <p class="text-sm text-success">+2.1% {$_("analytics.from_last_month")}</p>
        </div>
        <div class="w-12 h-12 bg-gradient-to-br {iconColors['heroicons:chart-bar']} rounded-xl flex items-center justify-center shadow-md group-hover:shadow-lg transition-shadow duration-300">
          <Icon icon="heroicons:chart-bar" class="w-6 h-6 text-white group-hover:scale-110 transition-transform duration-300" />
        </div>
      </div>
    </div>
    
    <div class="group relative overflow-hidden bg-gradient-to-br from-base-100 to-base-200/30 rounded-2xl shadow-md border border-base-300/50 p-5 hover:shadow-lg hover:scale-105 transition-all duration-300 backdrop-blur-sm" use:motionHover>
      <!-- Background decoration -->
      <div class="absolute top-0 right-0 w-16 h-16 opacity-5 group-hover:opacity-10 transition-opacity duration-300">
        <Icon icon="heroicons:clock" class="w-full h-full text-accent" />
      </div>
      
      <!-- Glow effect -->
      <div class="absolute inset-0 bg-gradient-to-r from-primary/5 to-secondary/5 opacity-0 group-hover:opacity-100 transition-opacity duration-300 rounded-2xl"></div>
      
      <div class="relative flex items-center justify-between">
        <div>
          <p class="text-sm font-medium text-base-content/70">{$_("analytics.avg_session")}</p>
          <p class="text-2xl font-bold text-base-content group-hover:text-primary transition-colors duration-300">{analyticsData.overview.avgSessionDuration}</p>
          <p class="text-sm text-success">+15.3% {$_("analytics.from_last_month")}</p>
        </div>
        <div class="w-12 h-12 bg-gradient-to-br {iconColors['heroicons:clock']} rounded-xl flex items-center justify-center shadow-md group-hover:shadow-lg transition-shadow duration-300">
          <Icon icon="heroicons:clock" class="w-6 h-6 text-white group-hover:scale-110 transition-transform duration-300" />
        </div>
      </div>
    </div>
  </div>
  
  <!-- Enhanced Charts and Data Section -->
  <div class="grid grid-cols-1 lg:grid-cols-3 gap-8">
    <!-- Main Chart -->
    <div class="lg:col-span-2 space-y-6">
      <!-- Revenue Trend Chart -->
      <div class="relative overflow-hidden bg-gradient-to-br from-base-100 to-base-200/30 rounded-2xl shadow-md border border-base-300/50 p-6 backdrop-blur-sm" use:motionInView={{ animation: 'fadeInLeft' }}>
        <!-- Background decoration -->
        <div class="absolute top-0 right-0 w-20 h-20 opacity-5">
          <Icon icon="heroicons:chart-bar" class="w-full h-full text-primary" />
        </div>
        
        <div class="relative flex items-center justify-between mb-6">
          <h2 class="text-lg font-semibold text-base-content">{$_("analytics.revenue_trend")}</h2>
          <!-- Metric selector -->
          <div class="relative metric-selector">
            <button 
              class="px-3 py-1 text-sm font-medium text-base-content/70 bg-base-200 border border-base-300 rounded-lg hover:bg-base-300 focus:outline-none focus:ring-2 focus:ring-primary transition-colors duration-200"
              on:click={toggleMetricSelect}
            >
              {metricOptions.find(opt => opt.value === selectedMetric)?.label || $_("analytics.revenue")}
              <Icon icon="heroicons:chevron-down" class="w-4 h-4 ml-1 inline" />
            </button>
            {#if showMetricSelect}
              <div class="absolute top-full mt-1 bg-base-100 border border-base-300 rounded-lg shadow-lg z-50 min-w-32">
                {#each metricOptions as item}
                  <button 
                    class="w-full px-3 py-2 text-left text-sm hover:bg-base-200 {item.value === selectedMetric ? 'bg-primary/10 text-primary' : 'text-base-content/70'} transition-colors duration-200"
                    on:click={() => selectMetric(item.value)}
                  >
                    {item.label}
                  </button>
                {/each}
              </div>
            {/if}
          </div>
        </div>
        
        <!-- Chart placeholder -->
        <div class="h-64">
          <AnalyticsChart 
            type="line" 
            metric={selectedMetric} 
            period="monthly" 
            height="h-64"
          />
        </div>
      </div>
      
    </div>
    
    <!-- Sidebar -->
    <div class="space-y-6">
      <!-- Quick Stats -->
      <div class="relative overflow-hidden bg-gradient-to-br from-base-100 to-base-200/30 rounded-2xl shadow-md border border-base-300/50 p-6 backdrop-blur-sm" use:motionInView={{ animation: 'fadeInRight' }}>
        <!-- Background decoration -->
        <div class="absolute top-0 right-0 w-20 h-20 opacity-5">
          <Icon icon="heroicons:chart-bar" class="w-full h-full text-secondary" />
        </div>
        
        <div class="relative flex items-center justify-between mb-6">
          <h2 class="text-lg font-semibold text-base-content">{$_("analytics.quick_stats")}</h2>
          <div class="flex items-center space-x-2 text-sm text-base-content/60">
            <Icon icon="heroicons:arrow-path" class="w-4 h-4" />
            <span>selected targets</span>
          </div>
        </div>
        <div>
          <!-- skyplot -->
          <div class="relative mt-6">
              <div class="mt-4">
              <label for="targets" class="block text-sm font-medium text-base-content">Targets (comma-separated):</label>
              <input
                id="targets"
                type="text"
                bind:value={targetsInput}
                placeholder="e.g., M31, M45, M42"
                class="input input-bordered w-full mt-2"
              />
  
              <label for="start_time" class="block text-sm font-medium text-base-content mt-4">Start Time:</label>
              <input
                id="start_time"
                type="datetime-local"
                bind:value={startTimeInput}
                class="input input-bordered w-full mt-2"
              />
  
              <button
                on:click={updateSkyplot}
                class="btn btn-primary mt-4"
              >
                Update Skyplot
              </button>
              </div>
            <div class="mt-4">
              <img
                  src={`http://192.168.1.237:7007/skyplot?${targetsInput
                  .split(',')
                  .map(target => `targets=${encodeURIComponent(target.trim())}`)
                  .join('&')}&start_time=${encodeURIComponent(startTimeInput)}`}
                alt="Skyplot Graph"
                class="w-full h-auto rounded-lg shadow-md border border-base-300/50"
              />
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</div>

<svelte:window on:click={handleClickOutside} /> 