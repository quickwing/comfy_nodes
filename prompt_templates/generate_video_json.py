class GenerateVideoJson:
    def __init__(self):
        pass
    
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "text": ("STRING", {"forceInput": True}),
            },
        }
 
    RETURN_TYPES = ("MESSAGES",)
    RETURN_NAMES = ("messages",)
 
    FUNCTION = "__call__"
 
    #OUTPUT_NODE = False
 
    CATEGORY = "sim/lm/prompts"
 
    def __call__(self, *args, **kwargs):
        ''' 
        Prompt local model
        '''
        messages = []
        messages.append({"role": "system", "content": "You are a helpful assistant that outputs only JSON objects. You are careful to not include any strig and your response will be used in a larger pipeline and must be valid JSON."})
        instruct = '''
            I want you to act as a presentation structure expert. I will provide a text document, and you should convert its content into a structured JSON format suitable for a video presentation. Think of it as a documentary style presentation with visual assistance with graphs and charts. 

            The JSON structure should follow this format:

            ```jsx
            {
            "slides": [
                {
                "slideType": string,  // Available types listed below
                "duration": number,   // Duration in frames (30fps)
                "icon": string,      // Optional: Lucide icon name
                "title": string,     // Optional: Slide title
                "theme": string,     // Optional: "blue" or "red"
                "audio": string,     // Optional: Path to audio file
                "slideNarration": string, //what the narrator should say to explain this slide. 
                ... // Additional properties based on slideType
                }
            ],
            "source": string        // Source citation
            }

            ```

            Available slideTypes and their specific properties:

            1. "introSlide":

            ```jsx
            {
            "slideType": "introSlide",
            "duration": 150,
            "title": string,
            "slideNarration": string,
            "subtitle": string
            }

            ```

            1. "statsGrid":

            ```jsx
            {
            "slideType": "statsGrid",
            "duration": 180,
            "icon": string,
            "title": string,
            "slideNarration": string,
            "stats": [
                { "region": string, "value": string },
                // ... more stats
            ]
            }

            ```

            1. "bigStat":

            ```jsx
            {
            "slideType": "bigStat",
            "duration": 120,
            "icon": string,
            "title": string,
            "slideNarration": string,
            "preText": string,
            "value": string,
            "postText": string
            }

            ```

            1. "statsList":

            ```jsx
            {
            "slideType": "statsList",
            "duration": 150,
            "icon": string,
            "title": string,
            "slideNarration": string,
            "heading": string,
            "stats": [
                { "label": string, "value": string },
                // ... more stats
            ]
            }

            ```

            1. "barChart":

            ```jsx
            {
            "slideType": "barChart",
            "duration": 180,
            "icon": string,
            "title": string,
            "slideNarration": string,
            "data": [
                { "name": string, "value": number },
                // ... more data points
            ],
            "config": {
                "xAxis": string,
                "yAxis": string,
                "maxValue": number,  // Optional
                "barColor": string   // Optional
            }
            }

            ```

            1. “pieChart”:

            ```jsx
            {
            slideType: "pieChart",
            duration: 180,
            icon: string,
            title: string,
            data: [
                { name: string, value: float},
                // ... more data points
            ],
            config: {
                colors: ['#2563eb', '#7c3aed', '#db2777'], // Optional custom colors, must be the same number as data points
                showPercent: true,
                showLegend: true
            }
            }
            ```

            Guidelines for conversion:

            1. Identify key sections, statistics, and data points from the PDF
            2. Choose appropriate slideTypes based on content:
                - Use "introSlide" for introductions and context
                - Use "statsGrid" for 2-4 related statistics
                - Use "bigStat" for emphasizing a single important number
                - Use "statsList" for multiple related statistics
                - Use "barChart" for comparing numerical data across categories
            3. For each slide:
                - Choose relevant Lucide icons when applicable
                - Break down complex information into digestible chunks
                - Maintain a logical flow between slides
                - Write slide narration on what the speaker should say when presenting the slide. The tone should be informal.
            4. Ensure:
                - Clear and concise titles
                - Accurate data representation
                - Proper source citation
                - Logical progression of information
            5. For the narration:
                - The narration should delve into explanation without saying things like: on this slide, this chart etc. The narration should simply explain the material being presented. It should be explained so that people listening around without video should be able to follow

            Start by starting a problem or asking a question to the audience that is intriguing. 

            Please structure a JSON with the provided data

            Example Conversion:
            From text:
            "A recent study found varying detection rates across regions: Europe (28%), North America (22%), Latin America (21%), and Asia/Africa (20%)."

            To JSON:

            ```jsx
            [{
            "slideType": "barChart",
            "duration": 180,
            "icon": "BarChart",
            "slideNarration": "A recent study found that Europe has the highest detection rate at 28% followed by North America. This is higher than Latin America and Asia",
            "title": "Detection Rates by Region",
            "data": [
                { "name": "Europe", "value": 28 },
                { "name": "North America", "value": 22 },
                { "name": "Latin America", "value": 21 },
                { "name": "Asia/Africa", "value": 20 }
            ],
            "config": {
                "xAxis": "Region",
                "yAxis": "Detection Rate (%)",
                "maxValue": 30
            }
            }]

            ```

            Please create a structured presentation JSON following these guidelines using the provided references. 

            There should be 3 slides in the output.

            Here is the text:

        '''

        user_message = instruct + kwargs["text"]
        messages.append({"role": "user", "content": user_message})

        return (messages,)