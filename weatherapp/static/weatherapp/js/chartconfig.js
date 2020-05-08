var chartConfig = function(xminvalue, xmaxvalue, temp_list, rain_list, pressure_list, winds_list, axisnames){
    var myConfig = {
        graphset: [ {
        "type":"mixed",
        "utc":true,
        "plot": {
                "tooltip": {
                            "visible": false
                          },
                },
        "scale-x":{
                  "min-value": xminvalue, 
                  "max-value": xmaxvalue, 
                  "step":10800000,
                  "transform":{
                                "type":"date",
                                "all":"%m/%d/%y<br>%H:%i" 
                            },
                  "guide":{
                    "visible":true,
                    "line-color":"#F2F2F2",
                    "line-style":"solid",
                    "line-width":1,
                    "alpha":0.5
                  },
                  'max-items': 18,
                  "item":{
                    "font-size":14
                  }
                },
        'scale-y': {
                    'label': {
                      'text': axisnames[0],
                      'fontSize': 14
                    },
                    'guide': { 
                        lineColor: '#F2F2F2'
                      }
                  },
        'scale-y-2': {
                      'minValue': 0,
                      'maxValue': 5,
                      'label': {
                        'text': axisnames[1],
                        'fontSize': 14
                      },
                      'guide': { 
                        'visible': false
                      }
                    },
        'crosshair-x' : { 'lineColor': "#565656",
                          'lineStyle': "dashed",
                          'lineWidth': 2,
                          'alpha': 0.5,
                          'plotLabel': { //label assoicated to data points
                                      'backgroundColor': "#ffffff",
                                      'borderColor': "#d2d2d2",
                                      'borderRadius': "5px",
                                      'bold': true,
                                      'fontSize': "12px",
                                      'fontColor': "#111",
                                      'shadowDistance': 2,
                                      'shadowAlpha': 0.4,
                                      
                                    },
                          'scaleLabel': { //label associated to scaleX index
                                      'bold': true,
                                      'backgroundColor': "#787878",
                                      'borderRadius': 3,
                                      'fontColor': "#eaeaea",
                                      'fontSize': "12px",
                                      'callout': true,
                                      'paddingTop': 2
                                    },
                          'marker': {
                            'visible': false 
                          }
                        },
    
        "series":[  {
                      'type': 'line',
                      'values': temp_list,
                      'text': axisnames[0],
                      'lineColor': '#FF0000',
                      'marker': {
                        'background-color': '#FF0000' 
                      }
                    } 
                  , {
                    'type': 'bar',
                    'values': rain_list ,
                    'text': axisnames[1] ,
                    'scales': 'scale-x, scale-y-2',
                    'backgroundColor': '#2E9AFE',
                    
                  } ]
        },
        {
            "type":"mixed",
            "utc":true,
            "plot": {
                    "tooltip": {
                                "visible": false
                              },
                    },
            "scale-x":{
                      "min-value": xminvalue, 
                      "max-value": xmaxvalue, 
                      "step":10800000,
                      "transform":{
                                    "type":"date",
                                    "all":"%m/%d/%y<br>%H:%i" 
                                },
                      "guide":{
                        "visible":true,
                        "line-color":"#F2F2F2",
                        "line-style":"solid",
                        "line-width":1,
                        "alpha":0.5
                      },
                      'max-items': 18,
                      "item":{
                        "font-size":14
                      }
                    },
            'scale-y': {
                        'minValue': 720,
                        'maxValue': 800,
                        'label': {
                          'text': axisnames[2],
                          'fontSize': 14
                        },
                        'guide': { 
                            lineColor: '#F2F2F2'
                          }
                      },
            'scale-y-2': {
                          'minValue': 0,
                          'maxValue': 20,
                          'label': {
                            'text': axisnames[3],
                            'fontSize': 14
                          },
                          'guide': { 
                            'visible': false
                          }
                        },
            'crosshair-x' : { 'lineColor': "#565656",
                              'lineStyle': "dashed",
                              'lineWidth': 2,
                              'alpha': 0.5,
                              'plotLabel': { //label assoicated to data points
                                          'backgroundColor': "#ffffff",
                                          'borderColor': "#d2d2d2",
                                          'borderRadius': "5px",
                                          'bold': true,
                                          'fontSize': "12px",
                                          'fontColor': "#111",
                                          'shadowDistance': 2,
                                          'shadowAlpha': 0.4,
                                          
                                        },
                              'scaleLabel': { //label associated to scaleX index
                                          'bold': true,
                                          'backgroundColor': "#787878",
                                          'borderRadius': 3,
                                          'fontColor': "#eaeaea",
                                          'fontSize': "12px",
                                          'callout': true,
                                          'paddingTop': 2
                                        },
                              'marker': {
                                'visible': false 
                              }
                            },
        
            "series":[  {
                          'type': 'line',
                          'values': pressure_list,
                          'text': axisnames[2],
                          'lineColor': '#2E9AFE',
                          'marker': {
                            'background-color': '#2E9AFE' 
                          }
                        } 
                      , {
                        'type': 'bar',
                        'values': winds_list ,
                        'text': axisnames[3] ,
                        'scales': 'scale-x, scale-y-2',
                        'backgroundColor': '#01DF01',
                        
                      } ]
            }
    ]  
                }; 
    return myConfig;
 }
    
 