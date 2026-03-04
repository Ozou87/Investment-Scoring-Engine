import { useState } from "react";
import { Search, TrendingUp, Loader2, AlertCircle } from "lucide-react";
import FinalScore from "@/components/FinalScore";
import ScoreCard from "@/components/ScoreCard";

interface AnalysisData {
  ticker: string;
  company_name: string;
  sector: string;
  scores: {
    fundamentals: {
      revenue_score: number;
      operating_margin_score: number;
      debt_to_equity_score: number;
      free_cash_flow_score: number;
      fundamentals_score: number;
    };
    valuation: {
      pe_score: number;
      forward_pe_score: number;
      ev_ebitda_score: number;
      ps_score: number;
      price_fcf_score: number;
      valuation_score: number;
    };
    moat: {
      roic_score: number;
      fcf_3y_cagr_score: number;
      r_and_d_to_revenue_score: number;
      moat_score: number;
    };
    final_score: number;
  };
}

const API_URL = "http://localhost:5000";

const Index = () => {
  const [ticker, setTicker] = useState("");
  const [data, setData] = useState<AnalysisData | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleAnalyze = async () => {
    const trimmed = ticker.trim().toUpperCase();
    if (!trimmed) return;

    setLoading(true);
    setError(null);
    setData(null);

    try {
      const res = await fetch(`${API_URL}/analyze?ticker=${trimmed}`);
      if (res.status === 404) {
        setError(`Ticker "${trimmed}" not found. Please check and try again.`);
        return;
      }
      if (!res.ok) {
        setError("Something went wrong. Please try again later.");
        return;
      }
      const json = await res.json();
      setData(json);
    } catch {
      setError("Failed to connect to the server. Please try again.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-background">
      {/* Top bar */}
      <header className="border-b border-border">
        <div className="max-w-5xl mx-auto px-4 py-4 flex items-center gap-3">
          <TrendingUp className="h-5 w-5 text-primary" />
          <span className="font-semibold text-foreground tracking-tight">StockScope</span>
          <span className="text-xs text-muted-foreground ml-1">Investment Analyzer</span>
        </div>
      </header>

      <main className="max-w-5xl mx-auto px-4 py-10 space-y-10">
        {/* Search */}
        <div className="flex justify-center">
          <div className="flex items-center gap-2 w-full max-w-md">
            <div className="relative flex-1">
              <Search className="absolute left-3 top-1/2 -translate-y-1/2 h-4 w-4 text-muted-foreground" />
              <input
                type="text"
                placeholder="Enter ticker (e.g. AAPL)"
                value={ticker}
                onChange={(e) => setTicker(e.target.value.toUpperCase())}
                onKeyDown={(e) => e.key === "Enter" && handleAnalyze()}
                className="w-full rounded-lg border border-input bg-secondary pl-10 pr-4 py-2.5 text-sm font-mono text-foreground placeholder:text-muted-foreground focus:outline-none focus:ring-2 focus:ring-ring"
              />
            </div>
            <button
              onClick={handleAnalyze}
              disabled={loading || !ticker.trim()}
              className="rounded-lg bg-primary px-5 py-2.5 text-sm font-semibold text-primary-foreground hover:opacity-90 transition-opacity disabled:opacity-40"
            >
              {loading ? <Loader2 className="h-4 w-4 animate-spin" /> : "Analyze"}
            </button>
          </div>
        </div>

        {/* Loading */}
        {loading && (
          <div className="flex flex-col items-center gap-3 py-16 text-muted-foreground">
            <Loader2 className="h-8 w-8 animate-spin text-primary" />
            <span className="text-sm">Analyzing {ticker.trim().toUpperCase()}...</span>
          </div>
        )}

        {/* Error */}
        {error && (
          <div className="flex items-center gap-3 justify-center rounded-lg border border-destructive/30 bg-destructive/10 px-5 py-4 max-w-md mx-auto">
            <AlertCircle className="h-5 w-5 text-destructive shrink-0" />
            <span className="text-sm text-destructive">{error}</span>
          </div>
        )}

        {/* Results */}
        {data && (
          <div className="space-y-8 animate-in fade-in-0 slide-in-from-bottom-4 duration-500">
            <FinalScore
              score={data.scores.final_score}
              companyName={data.company_name}
              ticker={data.ticker}
              sector={data.sector}
            />

            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
              <ScoreCard
                icon="🏗️"
                title="Fundamentals"
                score={data.scores.fundamentals.fundamentals_score}
                items={[
                  { label: "Revenue Growth", score: data.scores.fundamentals.revenue_score },
                  { label: "Operating Margin", score: data.scores.fundamentals.operating_margin_score },
                  { label: "Debt / Equity", score: data.scores.fundamentals.debt_to_equity_score },
                  { label: "Free Cash Flow", score: data.scores.fundamentals.free_cash_flow_score },
                ]}
              />
              <ScoreCard
                icon="💰"
                title="Valuation"
                score={data.scores.valuation.valuation_score}
                note="Lower = cheaper vs sector"
                items={[
                  { label: "P/E", score: data.scores.valuation.pe_score },
                  { label: "Forward P/E", score: data.scores.valuation.forward_pe_score },
                  { label: "EV / EBITDA", score: data.scores.valuation.ev_ebitda_score },
                  { label: "P/S", score: data.scores.valuation.ps_score },
                  { label: "P / FCF", score: data.scores.valuation.price_fcf_score },
                ]}
              />
              <ScoreCard
                icon="🏰"
                title="Moat"
                score={data.scores.moat.moat_score}
                items={[
                  { label: "ROIC", score: data.scores.moat.roic_score },
                  { label: "FCF 3Y CAGR", score: data.scores.moat.fcf_3y_cagr_score },
                  { label: "R&D / Revenue", score: data.scores.moat.r_and_d_to_revenue_score },
                ]}
              />
            </div>
          </div>
        )}

        {/* Empty state */}
        {!data && !loading && !error && (
          <div className="text-center py-20 text-muted-foreground">
            <p className="text-sm">Enter a stock ticker above to get started</p>
          </div>
        )}
      </main>
    </div>
  );
};

export default Index;
