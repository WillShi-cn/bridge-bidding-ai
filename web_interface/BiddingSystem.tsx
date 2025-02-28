import { useState } from 'react';
import { evaluateBid, generateDeal } from '@/utils/bridgeLogic';
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";

export function BiddingSystem() {
  const [deal, setDeal] = useState(generateDeal());
  const [biddingHistory, setBiddingHistory] = useState<string[]>([]);
  const [currentBid, setCurrentBid] = useState('');

  const handleBid = () => {
    if (evaluateBid([...biddingHistory, currentBid])) {
      setBiddingHistory([...biddingHistory, currentBid]);
      setCurrentBid('');
    }
  };

  return (
    <div className="space-y-4">
      <div className="grid grid-cols-4 gap-4 mb-4">
        {deal.map((hand, index) => (
          <div key={index} className="bg-white p-4 rounded">
            <h3 className="font-semibold">玩家 {index + 1}</h3>
            <p>{hand.join(' ')}</p>
          </div>
        ))}
      </div>
      
      <div className="flex gap-2">
        <Input 
          value={currentBid}
          onChange={(e) => setCurrentBid(e.target.value.toUpperCase())}
          placeholder="输入叫品（如1NT）"
        />
        <Button onClick={handleBid}>叫牌</Button>
      </div>
      
      <div className="bg-gray-50 p-4 rounded">
        <h3 className="font-semibold mb-2">叫牌过程：</h3>
        <div className="flex gap-2 flex-wrap">
          {biddingHistory.map((bid, index) => (
            <span key={index} className="bg-blue-100 px-2 py-1 rounded">
              {bid}
            </span>
          ))}
        </div>
      </div>
    </div>
  );
}