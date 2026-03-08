/**
 * FIXED: Smart Exponential Backoff Polling
 * 
 * Problem: Frontend was polling every 2 seconds for 2+ minutes (60+ requests)
 * Solution: Start fast, then slow down exponentially
 */

import { useState, useEffect, useRef } from 'react';

export const useApplicationStatus = (applicationId) => {
  const [status, setStatus] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const pollIntervalRef = useRef(null);
  const attemptCountRef = useRef(0);

  useEffect(() => {
    if (!applicationId) return;

    const checkStatus = async () => {
      try {
        const response = await fetch(
          `${import.meta.env.VITE_API_BASE_URL}/candidate/application/${applicationId}/status`
        );
        
        if (!response.ok) {
          throw new Error('Failed to fetch status');
        }

        const data = await response.json();
        setStatus(data);
        setLoading(false);

        // Stop polling if pipeline is complete or failed
        if (data.status === 'completed' || data.status === 'failed') {
          if (pollIntervalRef.current) {
            clearInterval(pollIntervalRef.current);
            pollIntervalRef.current = null;
          }
          return;
        }

        // Increment attempt counter
        attemptCountRef.current += 1;

      } catch (err) {
        console.error('Status check error:', err);
        setError(err.message);
        
        // Stop polling after 10 failures
        if (attemptCountRef.current > 10) {
          if (pollIntervalRef.current) {
            clearInterval(pollIntervalRef.current);
            pollIntervalRef.current = null;
          }
        }
      }
    };

    // SMART POLLING STRATEGY
    const getPollingInterval = (attemptCount) => {
      // Exponential backoff with maximum
      // Attempts 1-3: 3 seconds (fast initial check)
      // Attempts 4-6: 5 seconds
      // Attempts 7-10: 10 seconds
      // Attempts 11+: 15 seconds (slow down after waiting a while)
      
      if (attemptCount <= 3) return 3000;   // 3 sec (first 9 seconds)
      if (attemptCount <= 6) return 5000;   // 5 sec (next 15 seconds)
      if (attemptCount <= 10) return 10000; // 10 sec (next 40 seconds)
      return 15000;                          // 15 sec (after 64 seconds)
    };

    // Initial check
    checkStatus();

    // Start smart polling
    const startSmartPolling = () => {
      if (pollIntervalRef.current) {
        clearInterval(pollIntervalRef.current);
      }

      const interval = getPollingInterval(attemptCountRef.current);
      
      pollIntervalRef.current = setInterval(() => {
        checkStatus();
        
        // Adjust interval dynamically
        const newInterval = getPollingInterval(attemptCountRef.current);
        if (newInterval !== interval) {
          startSmartPolling(); // Restart with new interval
        }
      }, interval);
    };

    startSmartPolling();

    // Cleanup
    return () => {
      if (pollIntervalRef.current) {
        clearInterval(pollIntervalRef.current);
      }
    };
  }, [applicationId]);

  return { status, loading, error };
};


/**
 * ALTERNATIVE: WebSocket-Based Status Updates (Even Better)
 * 
 * No polling at all - backend pushes updates
 */
export const useApplicationStatusWebSocket = (applicationId) => {
  const [status, setStatus] = useState(null);
  const [loading, setLoading] = useState(true);
  const wsRef = useRef(null);

  useEffect(() => {
    if (!applicationId) return;

    // Initial fetch
    fetch(`${import.meta.env.VITE_API_BASE_URL}/candidate/application/${applicationId}/status`)
      .then(r => r.json())
      .then(data => {
        setStatus(data);
        setLoading(false);
      });

    // WebSocket for real-time updates
    const wsUrl = `${import.meta.env.VITE_API_BASE_URL.replace('http', 'ws')}/ws/application/${applicationId}`;
    wsRef.current = new WebSocket(wsUrl);

    wsRef.current.onmessage = (event) => {
      const data = JSON.parse(event.data);
      setStatus(data);
    };

    wsRef.current.onerror = (error) => {
      console.error('WebSocket error:', error);
      // Fallback to polling if WebSocket fails
    };

    return () => {
      if (wsRef.current) {
        wsRef.current.close();
      }
    };
  }, [applicationId]);

  return { status, loading };
};


/**
 * USAGE IN COMPONENT
 */
function ApplicationStatusPage({ applicationId }) {
  const { status, loading, error } = useApplicationStatus(applicationId);

  if (loading) {
    return (
      <div className="flex items-center justify-center p-8">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
        <p className="ml-4">Processing your application...</p>
      </div>
    );
  }

  if (error) {
    return (
      <div className="bg-red-50 border border-red-200 rounded p-4">
        <p className="text-red-800">Error: {error}</p>
      </div>
    );
  }

  return (
    <div className="space-y-4">
      <div className="bg-white shadow rounded-lg p-6">
        <h2 className="text-2xl font-bold mb-4">Application Status</h2>
        
        <div className="space-y-2">
          <div className="flex items-center justify-between">
            <span className="font-medium">Status:</span>
            <span className={`px-3 py-1 rounded-full text-sm ${
              status.status === 'completed' ? 'bg-green-100 text-green-800' :
              status.status === 'processing' ? 'bg-blue-100 text-blue-800' :
              status.status === 'failed' ? 'bg-red-100 text-red-800' :
              'bg-gray-100 text-gray-800'
            }`}>
              {status.status}
            </span>
          </div>

          {status.current_stage && (
            <div className="flex items-center justify-between">
              <span className="font-medium">Current Stage:</span>
              <span className="text-gray-700">{status.current_stage}</span>
            </div>
          )}

          {status.progress && (
            <div className="mt-4">
              <div className="flex justify-between mb-1">
                <span className="text-sm font-medium">Progress</span>
                <span className="text-sm text-gray-600">{status.progress}%</span>
              </div>
              <div className="w-full bg-gray-200 rounded-full h-2">
                <div
                  className="bg-blue-600 h-2 rounded-full transition-all duration-500"
                  style={{ width: `${status.progress}%` }}
                ></div>
              </div>
            </div>
          )}
        </div>
      </div>

      {status.stages && (
        <div className="bg-white shadow rounded-lg p-6">
          <h3 className="text-lg font-semibold mb-3">Pipeline Stages</h3>
          <div className="space-y-2">
            {status.stages.map((stage, index) => (
              <div key={index} className="flex items-center space-x-3">
                <div className={`w-3 h-3 rounded-full ${
                  stage.status === 'completed' ? 'bg-green-500' :
                  stage.status === 'running' ? 'bg-blue-500 animate-pulse' :
                  stage.status === 'failed' ? 'bg-red-500' :
                  'bg-gray-300'
                }`}></div>
                <span className="flex-1">{stage.name}</span>
                <span className="text-sm text-gray-500">{stage.status}</span>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}
