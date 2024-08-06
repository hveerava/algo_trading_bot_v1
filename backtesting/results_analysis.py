import matplotlib.pyplot as plt
import logging

class ResultsAnalysis:
    @staticmethod
    def plot_returns(returns):
        try:
            plt.figure(figsize=(12, 6))
            plt.plot(returns, label='Strategy Returns', color='blue')
            plt.xlabel('Time')
            plt.ylabel('Returns')
            plt.title('Strategy Returns Over Time')
            plt.legend()
            plt.grid(True)
            plt.show()
            logging.info("Returns plot generated successfully")
        except Exception as e:
            logging.error(f"Error generating returns plot: {str(e)}")
