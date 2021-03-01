def get_td(ip_address):
    return {
        "@context": [
            "https://www.w3.org/2019/wot/td/v1",
            {"@language": "en"}
        ],
        'id': 'de:tum:ei:esi:phat:{}'.format(ip_address),
        'title': 'ScrollPhat HD',
        'description': 'A scroll-phat-hd that can be remotely controlled.',
        "securityDefinitions": {"nosec_sc": {"scheme": "nosec"}},
        "security": "nosec_sc",
        'properties': {
            'display_size': {
                "title": "The Display Size",
                "description": "Get the size/shape of the display. Returns a tuple containing the width and height of the display, after applying rotation.",
                "type": "object",
                "properties": {
                    "width" : {
                        "type" : "integer"
                    },
                    "height" : {
                        "type" : "integer"
                    }
                },
                "readOnly": True,
                "forms": [{
                    "href": "http://{}/properties/display_size".format(ip_address),
                    "contentType": "application/json",
                    "op": ["readproperty"]
                }]
            },
            'buffer_size': {
                "title": "The Buffer Size",
                "description": "    Get the size/shape of the internal buffer. Returns a tuple containing the width and height of the buffer.",
                "type": "object",
                "properties": {
                    "width" : {
                        "type" : "integer"
                    },
                    "height" : {
                        "type" : "integer"
                    }
                },
                "readOnly": True,
                "forms": [{
                    "href": "http://{}/properties/buffer_size".format(ip_address),
                    "contentType": "application/json",
                    "op": ["readproperty"]
                }]
            }
            
        },
        "actions": {
            "set_pixel": {
                "description": "Light a specific single pixel with a given brightness.",
                "safe":False,
                "idempotent":True,
                "input": {
                    "type": "object",
                    "required": ["x", "y", "brightness"],
                    "properties": {
                        "x": {
                            "type": "integer",
                            "minimum": 0,
                            "maximum": 17
                        },
                        "y": {
                            "type": "integer",
                            "minimum": 0,
                            "maximum": 1
                        },
                        "brightness": {
                            "type": "number",
                            "minimum": 0.0,
                            "maximum": 1.0    
                        }
                    },
                },
                "forms": [{
                    "href": "http://{}/actions/set_pixel".format(ip_address),
                    "contentType": "application/json",
                    "op": "invokeaction"
                }]
            },
            "write_string": {
                "description": "Write a string to the buffer. Calls draw_char for each character.",
                "safe":False,
                "idempotent":True,
                "input": {
                    "type": "object",
                    "required": ["string","x", "y", "brightness","monospaced"],
                    "properties": {
                        "string": {
                            "description": "The string to display.",
                            "type": "string"
                        },
                        "x": {
                            "description": "Offset x - distance of the string from the left of the buffer",
                            "type": "integer",
                            "minimum": 0,
                            "maximum": 17
                        },
                        "y": {
                            "description": "Offset x - distance of the string from the left of the buffer",
                            "type": "integer",
                            "minimum": 0,
                            "maximum": 1
                        },
                        "brightness": {
                            "type": "number",
                            "minimum": 0.0,
                            "maximum": 1.0    
                        },
                        "monospaced" : {
                            "type": "boolean"
                        }
                    },
                },
                "forms": [{
                    "href": "http://{}/actions/write_string".format(ip_address),
                    "contentType": "application/json",
                    "op": "invokeaction"
                }]
            },
            "write_char": {
                "description": "Write a single char to the buffer. Returns the x and y coordinates of the bottom left-most corner of the drawn character.",
                "safe":False,
                "idempotent":True,
                "input": {
                    "type": "object",
                    "required": ["string","o_x", "o_y", "brightness","monospaced"],
                    "properties": {
                        "char": {
                            "description": "Char to display- either an integer ordinal or a single letter",
                            "type": "string"
                        },
                        "o_x": {
                            "description": "Offset x - distance of the string from the left of the buffer",
                            "type": "integer",
                            "minimum": 0,
                            "maximum": 17
                        },
                        "o_y": {
                            "description": "Offset x - distance of the string from the left of the buffer",
                            "type": "integer",
                            "minimum": 0,
                            "maximum": 1
                        },
                        "brightness": {
                            "type": "number",
                            "minimum": 0.0,
                            "maximum": 1.0    
                        },
                        "monospaced" : {
                            "type": "boolean"
                        }
                    },
                },
                "forms": [{
                    "href": "http://{}/actions/write_char".format(ip_address),
                    "contentType": "application/json",
                    "op": "invokeaction"
                }]
            },
            "set_graph": {
                "description": "Plot a series of values into the display buffer.",
                "safe":False,
                "idempotent":True,
                "input": {
                    "type": "object",
                    "required": ["brightness","values"],
                    "properties": {
                        "values": {
                            "description": "A list of numerical values to display",
                            "type": "array",
                            "items" : {
                                "type": "number"
                            }
                        },
                        "x": {
                            "description": "x position of graph in display buffer (default 0)",
                            "type": "integer",
                            "minimum": 0,
                            "maximum": 17
                        },
                        "y": {
                            "description": "y position of graph in display buffer (default 0)",
                            "type": "integer",
                            "minimum": 0,
                            "maximum": 1
                        },
                        "brightness": {
                            "type": "number",
                            "minimum": 0.0,
                            "maximum": 1.0    
                        },
                        "width": {
                            "description": "Width of the graph (default is buffer 17),
                            "type": "integer",
                            "minimum": 0,
                            "maximum": 17
                        },
                        "height": {
                            "description": "Height of the graph (default is buffer 7)",
                            "type": "integer",
                            "minimum": 0,
                            "maximum": 7
                        }
                        
                    },
                },
                "forms": [{
                    "href": "http://{}/actions/write_char".format(ip_address),
                    "contentType": "application/json",
                    "op": "invokeaction"
                }]
            },

            "fill": {
                "description": "Fill an area of the display.",
                "safe": False,
                "idempotent": True,
                "input": {
                    "type": "object",
                    "required": ["brightness","x", "y"],
                    "properties": {
                        "x": {
                            "description": "Offset x - distance of the area from the left of the buffer.",
                            "type": "integer",
                            "minimum": 0,
                            "maximum": 17
                        },
                        "y": {
                            "description": "Offset y - distance of the area from the left of the buffer.",
                            "type": "integer",
                            "minimum": 0,
                            "maximum": 1
                        },
                        "brightness": {
                            "type": "number",
                            "minimum": 0.0,
                            "maximum": 1.0    
                        },
                        "width": {
                            "description": "Width of the area (default is buffer width)",
                            "type": "integer",
                            "minimum": 0,
                            "maximum": 17
                        },
                        "height": {
                            "description": "Height of the area (default is buffer height)",
                            "type": "integer",
                            "minimum": 0,
                            "maximum": 7
                        }
                     },
                },
                "forms": [{
                    "href": "http://{}/actions/fill".format(ip_address),
                    "contentType": "application/json",
                    "op": "invokeaction"
                }]
            },
            "clear_rect(": {
                "description": "Clear a rectangle.",
                "safe": False,
                "idempotent": True,
                "input": {
                    "type": "object",
                    "required": ["x", "y"],
                    "properties": {
                        "x": {
                            "description": "Offset x - distance of the area from the left of the buffer.",
                            "type": "integer",
                            "minimum": 0,
                            "maximum": 17
                        },
                        "y": {
                            "description": "Offset y - distance of the area from the left of the buffer.",
                            "type": "integer",
                            "minimum": 0,
                            "maximum": 1
                        },
                        "width": {
                            "description": "Width of the area (default is buffer 17)",
                            "type": "integer",
                            "minimum": 0,
                            "maximum": 17
                        },
                        "height": {
                            "description": "Height of the area (default is buffer 7)",
                            "type": "integer",
                            "minimum": 0,
                            "maximum": 7
                        }
                     },
                },
                "forms": [{
                    "href": "http://{}/actions/clear_rect".format(ip_address),
                    "contentType": "application/json",
                    "op": "invokeaction"
                }]
            },
            
            "clear": {
                "description": "clears all pixels.",
                "safe": False,
                "idempotent": True,
                "forms": [{
                    "href": "http://{}/actions/clear".format(ip_address),
                    "contentType": "application/json",
                    "op": "invokeaction"
                }]
            },
            "scroll" : {
                "description": "Scroll pHAT HD displays an 17x7 pixel window into the bufer, which starts at the left offset and wraps around. The x and y values are added to the internal scroll offset.",
                "input" : {
                    "type": "object",
                    "properties": {
                        "x": {
                            "description": "Amount to scroll on x-axis (default 1)",
                            "type": "integer",
                            
                        },
                        "y": {
                            "description": "Amount to scroll on y-axis (default 0)",
                            "type": "integer",
                        }
                    }
                },
                "forms": [{
                    "href": "http://{}/actions/scroll".format(ip_address),
                    "contentType": "application/json",
                    "op": "invokeaction"
                }]

            }
           
        }
    }
