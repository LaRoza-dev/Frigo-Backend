import uvicorn
import argparse

# parser = argparse.ArgumentParser(description="Select the stage of backend")
# parser.add_argument("-p","--production",action="store_true",help="for production")
# parser.add_argument("-d","--development", action='store_true',help="for development")

# args = parser.parse_args()

# if args.production and args.development:
#     parser.error("choose just one flag")
# elif args.production :
#     stage = "production"
# elif args.development:
#     stage = "development"
# else:
#     parser.error("see -h or --help to use correct flag.")
stage = "development"

if __name__ == "__main__":
    uvicorn.run("app:app", host="127.0.0.1", port=8000, reload=True)