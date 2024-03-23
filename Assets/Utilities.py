def Parse_Private():
    try:
        with open("Daddy-Bot-env/Assets/Private.txt", "r") as tokenFile:
            lines = tokenFile.readlines()
        
        # Initialize a dictionary to hold the values
        values = {}
        for line in lines:
            # Skip lines that do not contain ' = '
            if ' = ' not in line:
                continue
            key, value = line.strip().split(' = ')
            values[key] = value.strip("'")
        
        # Extract token and URL from the dictionary
        token = values.get('Token')
        URL = values.get('URL')
        
        if token is None or URL is None:
            raise ValueError("Token or URL not found in file")
        
        return token, URL
    