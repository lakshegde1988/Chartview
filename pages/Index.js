import { useEffect, useState } from 'react';
import CandlestickChart from '../components/CandlestickChart';
import TopBar from '../components/TopBar';
import BottomNav from '../components/BottomNav';

export default function Home() {
  const [stocks, setStocks] = useState([]);
  const [currentStockIndex, setCurrentStockIndex] = useState(0);
  const [ohlcData, setOhlcData] = useState([]);
  const [stockName, setStockName] = useState('');

  useEffect(() => {
    async function fetchStocks() {
      const response = await fetch('/api/stocks');
      const data = await response.json();
      setStocks(data);
      if (data.length > 0) {
        loadStockChart(data[0].symbol, data[0].name);
      }
    }
    fetchStocks();
  }, []);

  const loadStockChart = async (symbol, name) => {
    setStockName(name);
    setOhlcData([]);

    try {
      const response = await fetch(`/api/ohlc/${symbol}`);
      const data = await response.json();
      setOhlcData(data);
    } catch (error) {
      console.error('Error fetching OHLC data:', error);
    }
  };

  const handleNextStock = () => {
    const nextIndex = (currentStockIndex + 1) % stocks.length;
    setCurrentStockIndex(nextIndex);
    loadStockChart(stocks[nextIndex].symbol, stocks[nextIndex].name);
  };

  const handlePreviousStock = () => {
    const previousIndex = (currentStockIndex - 1 + stocks.length) % stocks.length;
    setCurrentStockIndex(previousIndex);
    loadStockChart(stocks[previousIndex].symbol, stocks[previousIndex].name);
  };

  return (
    <div className="relative min-h-screen bg-gray-100">
      <TopBar stockName={stockName} />

      <div className="container mx-auto mt-20 p-4">
        <div className="mt-4">
          <CandlestickChart ohlcData={ohlcData} />
        </div>
      </div>

      <BottomNav onPrevious={handlePreviousStock} onNext={handleNextStock} />
    </div>
  );
}
