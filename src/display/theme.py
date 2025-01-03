class AppTheme:
    # Primary Colors (Green)
    PRIMARY = "#4CAF50"
    PRIMARY_LIGHT = "#81C784"
    PRIMARY_DARK = "#388E3C"
    
    # Error Colors (Red)
    ERROR = "#F44336"
    ERROR_LIGHT = "#E57373"
    ERROR_DARK = "#D32F2F"
    
    # Warning Colors (Orange)
    WARNING = "#FF9800"
    WARNING_LIGHT = "#FFB74D"
    WARNING_DARK = "#F57C00"
    
    # Info Colors (Blue)
    INFO = "#2196F3"
    INFO_LIGHT = "#64B5F6"
    INFO_DARK = "#1976D2"
    
    # Neutral Colors
    WHITE = "#FFFFFF"
    LIGHT_GRAY = "#F5F5F5"
    GRAY = "#9E9E9E"
    BLACK = "#212121"
    
    @classmethod
    def configure_styles(cls, style):
        """Configure ttk styles with theme colors"""
        style.configure('Primary.TButton',
                       background=cls.PRIMARY,
                       foreground=cls.WHITE,
                       padding=(20, 10),
                       font=('Helvetica', 30, 'bold'))
        
        style.configure('Count.TButton',
                       background=cls.INFO,
                       foreground=cls.WHITE,
                       padding=(20, 10),
                       font=('Helvetica', 30, 'bold'))
        
        style.configure('Continue.TButton',
                       background=cls.PRIMARY,
                       foreground=cls.WHITE,
                       padding=(20, 10),
                       font=('Helvetica', 30, 'bold'))
                       
        style.configure('Reset.TButton',
                       background=cls.WARNING,
                       foreground=cls.WHITE,
                       padding=(20, 10),
                       font=('Helvetica', 30, 'bold'))
                       
        style.configure('Exit.TButton',
                       background=cls.ERROR,
                       foreground=cls.WHITE,
                       padding=(20, 10),
                       font=('Helvetica', 30, 'bold'))
                       
        style.configure('Counter.TLabel',
                       background=cls.LIGHT_GRAY,
                       foreground=cls.BLACK,
                       font=('Helvetica', 24, 'bold'),
                       padding=(10, 5))
        
        # Add vertical scale styling
        style.configure('Vertical.TScale',
                       background=cls.LIGHT_GRAY,
                       troughcolor=cls.PRIMARY_LIGHT,
                       lightcolor=cls.PRIMARY,
                       darkcolor=cls.PRIMARY_DARK)
        
        # Add specific styles for brightness control
        style.configure('Brightness.TFrame',
                       background=cls.LIGHT_GRAY,
                       relief='raised',
                       borderwidth=2)
        
        style.configure('Brightness.TLabel',
                       background=cls.LIGHT_GRAY,
                       foreground=cls.BLACK,
                       font=('Helvetica', 25, 'bold'),
                       padding=(5, 5))
        
        style.configure('Brightness.Vertical.TScale',
                       background=cls.LIGHT_GRAY,
                       troughcolor=cls.PRIMARY_LIGHT,
                       sliderlength=30,
                       sliderthickness=20,
                       relief='raised')
