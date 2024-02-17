from argparse import ArgumentParser
from analyser import BasketballAnalysis
        
        
def main():
    parser = ArgumentParser(prog= "FitnessTracker")
    parser.add_argument('-s', '--source', default='./WHATSAAP ASSIGNMENT.mp4')
    parser.add_argument('-md', '--model_dir', default='./models/yolov8l.pt')
    parser.add_argument('-sv', '--save_vid', default= 'Y')
    parser.add_argument('-p', '--play', default= 'Y')
    args = parser.parse_args()
    
    basketball_analysis = BasketballAnalysis(args)
    
    basketball_analysis.run_analysis()
    
if __name__ == "__main__":
    main()