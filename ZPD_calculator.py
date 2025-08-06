"""
ZPD Calculator - Adjusts question difficulty based on student performance

This code manages how hard or easy questions should be for each student.
It watches how well students do and tweaks the difficulty up or down.
Uses numpy for number crunching and type hints for better code clarity.
"""
from typing import List, Tuple, Optional
import numpy as np

class ZPDCalculator:
    def __init__(self, initial_zpd: float = 5.0):
        """
        Set up the calculator with a starting difficulty level.
        
        The ZPD score goes from 1.0 (super easy) to 10.0 (really hard).
        We start at 5.0 by default - right in the middle.
        """
        if not 1.0 <= initial_zpd <= 10.0:
            raise ValueError("Initial ZPD must be between 1.0 and 10.0")
            
        self.current_zpd = round(initial_zpd, 1)
        self.min_zpd = 1.0
        self.max_zpd = 10.0
        
        # Smoothing factors (0.0 to 1.0) - tuned for stable adaptation
        self.performance_alpha = 0.3  # Higher = faster response to performance changes
        self.zpd_beta = 0.15          # Lower = smoother ZPD transitions
        
        # Performance tracking state
        self.smoothed_performance = 0.5  # EMA of performance (0.0 to 1.0)
        self.performance_trend = 0.0     # Rate of performance change
        self.consecutive_successes = 0   # Tracks correct answer streaks

    def get_user_zpd(self) -> float:
        """
        Get the current ZPD (Zone of Proximal Development) score.
        """
        return self.current_zpd

    def calculate_performance_score(self, scores: List[float]):
        """
        Figure out how well the student is doing based on their recent answers.
        
        We care more about what they got right recently than a long time ago.
        Returns a number between 0.0 (all wrong) and 1.0 (all correct).
        
        For example, if they got [0.8, 0.9, 1.0] on their last three answers,
        we'll give more weight to that perfect 1.0 at the end.
        """
        if not scores:
            return 0.5  # Neutral score if no history
            
        # Create linear weights that increase with recency
        # Recent answers get up to 10x more weight than older ones
        weights = np.linspace(0.1, 1.0, len(scores))
        weighted_sum = sum(w * s for w, s in zip(weights, scores))
        
        # Ensure the result is within valid bounds
        return min(1.0, max(0.0, weighted_sum / sum(weights)))

    def update_user_zpd(self, performance_score: float) -> float:
        """
        Update the difficulty level based on how the student did.
        
        Takes their latest score (0.0 to 1.0) and adjusts the difficulty.
        If they're doing well, we make it harder. If they're struggling,
        we make it a bit easier.
        
        Returns the new difficulty level (ZPD score).
        """
        old_zpd = self.current_zpd
        
        # Update smoothed performance using Exponential Moving Average (EMA)
        # This helps reduce noise in the performance signal
        prev_smoothed = self.smoothed_performance
        self.smoothed_performance = (
            self.performance_alpha * performance_score + 
            (1 - self.performance_alpha) * prev_smoothed
        )
        
        # Track performance trend (first derivative of smoothed performance)
        # Positive trend indicates improving performance
        self.performance_trend = self.smoothed_performance - prev_smoothed
        
        # Calculate ZPD adjustment based on performance level
        adjustment = self._calculate_zpd_adjustment(performance_score)
        
        # Apply non-linear scaling to prevent large jumps in difficulty
        # Square root scaling makes large adjustments more conservative
        adjustment = np.sign(adjustment) * (abs(adjustment) ** 0.5) * 0.5
        
        # Update ZPD using EMA for smooth transitions
        # This prevents sudden changes in difficulty level
        target_zpd = old_zpd + adjustment
        self.current_zpd = round(
            max(self.min_zpd, min(self.max_zpd, 
                self.zpd_beta * target_zpd + 
                (1 - self.zpd_beta) * old_zpd
            )), 
            1  # Round to 1 decimal place for readability
        )
        
        # Log the update for debugging and monitoring
        self._log_zpd_update(old_zpd, performance_score, adjustment)
        
        return self.current_zpd
        
    def _calculate_zpd_adjustment(self, performance_score: float) -> float:
        """
        Figures out how much to adjust the ZPD based on how well the student did.
        
        The better they do, the more we increase the difficulty. If they're struggling,
        we'll make it a bit easier for them. We also give bonus points for getting
        multiple questions right in a row!
        """
        
        # If they did really well (90%+ correct)
        if performance_score >= 0.9:
            # Keep track of how many they've gotten right in a row
            self.consecutive_successes += 1
            
            # Base increase for doing well
            adjustment = 0.25
            
            # Extra boost for getting multiple right in a row
            # (but don't let it get out of hand - max 3 in a row count)
            streak_bonus = min(3, self.consecutive_successes) * 0.15
            
            return adjustment + streak_bonus
            
        # If they got it partially right (60-89%)
        elif performance_score >= 0.6:
            # Reset the streak counter - they didn't get it fully right
            self.consecutive_successes = 0
            
            # Calculate how close to 100% they were (0.0 to 0.3)
            how_close_to_perfect = performance_score - 0.6
            
            # Give a small boost based on how close to perfect they were
            partial_bonus = how_close_to_perfect * 0.4
            
            # Always give at least a small positive nudge
            return 0.1 + partial_bonus
            
        # If they didn't do so well (below 60%)
        else:
            # Reset the streak counter - they got it wrong
            self.consecutive_successes = 0
            
            # Figure out how far off they were (0.0 to 0.6)
            how_wrong = 0.6 - performance_score
            
            # Make it a bit easier, but don't drop too fast
            # Cap the penalty at 0.15 to prevent huge drops
            penalty = min(0.15, how_wrong * 0.3)
            
            # Return as negative to make it easier
            return -penalty
    
    def _log_zpd_update(self, old_zpd: float, performance_score: float, 
                       adjustment: float) -> None:
        """Log ZPD update information if debugging and monitoring needed."""
        print(f"[ZPD Update] "
              f"Old ZPD: {old_zpd:.1f} → New ZPD: {self.current_zpd:.1f}, "
              f"Performance: {performance_score:.2f} "
              f"(smoothed: {self.smoothed_performance:.2f}), "
              f"Trend: {self.performance_trend:+.3f}, "
              f"Adjustment: {adjustment:+.3f}")