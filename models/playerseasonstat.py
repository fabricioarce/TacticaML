from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class PlayerSeasonStat(Base):
    __tablename__ = 'player_season_stats'

    id = Column(String, primary_key=True, autoincrement=True)
    player_id = Column(String, ForeignKey('players.id'))
    team_season_id = Column(String, ForeignKey('team_season_stats.id'))

    # Relaciones
    team_season = relationship("TeamSeasonStat", back_populates="player_season_stats")
    player = relationship("Player", back_populates="season_stats")

    # Datos generales
    pos = Column(String)
    age = Column(Integer)

    # Goles y asistencias
    gls = Column(Integer)
    gplusa = Column(Integer)
    gminuspk = Column(Integer)
    pk = Column(Integer)
    pkatt = Column(Integer)

    # Tarjetas
    crdy = Column(Integer)
    crdr = Column(Integer)
    secondcrdy = Column(Integer)

    # xG y variantes
    xg = Column(Float)
    npxg = Column(Float)
    npxgpersh = Column(Float)
    glsminusxg = Column(Float)
    npgminusnpxg = Column(Float)

    npxg_xag = Column(Float)

    # Progresiones
    prgc = Column(Integer)
    prgr = Column(Integer)

    # Tiros
    sh = Column(Integer)
    sot = Column(Integer)
    sot_pct = Column(Float)
    sh_per90 = Column(Float)
    sot_per90 = Column(Float)
    g_sh = Column(Float)
    g_sot = Column(Float)
    dist = Column(Float)
    fk = Column(Integer)

    # Pases Total
    cmp = Column(Integer)
    att = Column(Integer)
    cmp_pct = Column(Float)
    totdist = Column(Float)
    prgdist = Column(Float)
    
        # short
    cmp_short = Column(Integer)
    att_short = Column(Integer)
    cmp_pct_short = Column(Float)

        # medium
    cmp_medium = Column(Integer)
    att_medium = Column(Integer)
    cmp_pct_medium = Column(Float)

        # long
    cmp_long = Column(Integer)
    att_locmp_long = Column(Integer)
    cmp_pct_locmp_long = Column(Float)
        
        # Expected
    ast = Column(Float) 
    xag = Column(Float)
    xa = Column(Float)
    aminusxag = Column(Float)
    kp = Column(Float)
    ft = Column(Float)
    ppa = Column(Float)
    crspa = Column(Float)
    prgp = Column(Float)

    # Pass type
    live = Column(Float)
    dead = Column(Float)
    pfk = Column(Float)
    tb = Column(Float)
    sw = Column(Float)
    crs = Column(Float)
    ti = Column(Float)
    ck = Column(Float)
    pass_off = Column(Float)
    blocks = Column(Float)

        # corners
    corner_in = Column(Float)
    corner_out = Column(Float)
    corner_str = Column(Float)

    # Otros campos (agrega los que necesites)
    passes = Column(Integer)
    tackles = Column(Integer)
    cards = Column(Integer)
    fatigue_level = Column(Integer)
    
    # goal and shot creation
    sca = Column(Integer)
    sca_per90 = Column(Float)
    sca_passlive = Column(Float)
    sca_passdead = Column(Float)
    sca_to = Column(Float)
    sca_sh = Column(Float)
    sca_fld = Column(Float)
    sca_def = Column(Float)
    gca = Column(Integer)
    gca_per90 = Column(Float)
    gca_passlive = Column(Float)
    gca_passdead = Column(Float)
    gca_sh = Column(Float)
    gca_to = Column(Float)
    gca_fld = Column(Float)
    gca_def = Column(Float)
    
    # Defensive actions
    tackles_tkl = Column(Integer)
    tackles_tklw = Column(Integer)
    def_3rd = Column(Integer)
    mid_3rd = Column(Integer)
    att_3rd = Column(Integer)
    challenges_tkl = Column(Integer)
    challenges_att = Column(Integer)
    tackles_tkl_percentage = Column(Float)
    challenges_lost = Column(Integer)
    def_blocks = Column(Integer)
    def_blocks_sh = Column(Integer)
    def_blocks_pass = Column(Integer)
    interceptions = Column(Integer)
    tklplusinterceptions = Column(Integer)
    clearences = Column(Integer)
    errors = Column(Integer)
    
    # Possesion 
    touches = Column(Integer)
    def_pen = Column(Integer)
    def_3rd = Column(Integer)
    mid_3rd = Column(Integer)
    att_3rd = Column(Integer)
    att_pen = Column(Integer)
    touches_live = Column(Integer)
    tale_on_att = Column(Integer)
    success = Column(Integer)
    success_pct = Column(Float)
    tkld = Column(Integer)
    tkld_pct = Column(Float)
    carries = Column(Integer)
    tot_dist = Column(Float)
    prg_dist = Column(Float)
    prgc = Column(Integer)
    one_third = Column(Integer)
    cpa = Column(Integer)
    mis = Column(Integer)
    dis = Column(Integer)
    
    # playing time
    mp = Column(Integer)
    min = Column(Integer)
    minpermp = Column(Float)
    min_pct = Column(Float)
    ninetys = Column(Float)
    starts = Column(Integer)
    minperstart = Column(Float)
    compl = Column(Integer)
    subs = Column(Integer)
    minpersub = Column(Float)
    unsub = Column(Integer)
    ppm = Column(Integer)
    ong = Column(Integer)
    onga = Column(Integer)
    plusminus = Column(Integer)
    plusminus_per90 = Column(Float)
    onoff = Column(Float)
    onxg = Column(Float)
    onxga = Column(Float)
    xgplusminus = Column(Float)
    xgplusminus_per90 = Column(Float)
    xg_onoff = Column(Float)
    
    # Miscellaneous
    
    crdy = Column(Integer)
    crdr = Column(Integer)
    secondcrdy = Column(Integer)
    fls = Column(Integer)
    fld = Column(Integer)
    off = Column(Integer)
    crs = Column(Integer)
    interceptions = Column(Integer)
    tkl_won = Column(Integer)
    pk_won = Column(Integer)
    og = Column(Integer)
    recov = Column(Integer)
    won = Column(Integer)
    lost = Column(Integer)
    won_pct = Column(Float)
    