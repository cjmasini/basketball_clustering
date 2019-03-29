import pandas as pd
import numpy as np
import pickle
from constants import *
from glicko2 import Player
from kenpom import create_matrix


def update_stats(team_stats, team_results, glicko, kenpom_matrix, row):
    #Update glicko scores
    w_rating, l_rating = glicko[row.WTeamID].getRating(), glicko[row.LTeamID].getRating()
    w_rd, l_rd = glicko[row.WTeamID].getRd(), glicko[row.LTeamID].getRd()

    glicko[row.WTeamID].update_player([l_rating], [l_rd], [1])
    glicko[row.LTeamID].update_player([w_rating], [w_rd], [0])

    #Update location information
    team_results[row.WTeamID].append({'opponent': row.LTeamID, 'result': 1, 'loc': row.WLoc})
    if row.WLoc == 'A':
        l = 'H'
    elif row.WLoc == 'H':
        l = 'A'
    else:
        l = 'N'
    team_results[row.LTeamID].append({'opponent': row.WTeamID, 'result': 0, 'loc': l})

    #Update all statistics found in team stats
    poss_0 = row.LFGA-row.LOR+row.LTO+(.4*row.LFTA)
    poss_1 = row.WFGA-row.WOR+row.WTO+(.4*row.WFTA)
    team_stats[row.LTeamID]['possesions'] += poss_0
    team_stats[row.WTeamID]['possesions'] += poss_1
    team_stats[row.LTeamID]['games'] += 1.0
    team_stats[row.WTeamID]['games'] += 1.0
    team_stats[row.LTeamID]['points'] += row.LScore
    team_stats[row.WTeamID]['points'] += row.WScore
    team_stats[row.LTeamID]['fgm'] += row.LFGM
    team_stats[row.WTeamID]['fgm'] += row.WFGM
    team_stats[row.LTeamID]['fga'] += row.LFGA
    team_stats[row.WTeamID]['fga'] += row.WFGA
    team_stats[row.LTeamID]['fgm3'] += row.LFGM3
    team_stats[row.WTeamID]['fgm3'] += row.WFGM3
    team_stats[row.LTeamID]['fga3'] += row.LFGA3
    team_stats[row.WTeamID]['fga3'] += row.WFGA3
    team_stats[row.LTeamID]['fta'] += row.LFTA
    team_stats[row.WTeamID]['fta'] += row.WFTA
    team_stats[row.LTeamID]['ftm'] += row.LFTM
    team_stats[row.WTeamID]['ftm'] += row.WFTM
    team_stats[row.LTeamID]['or'] += row.LOR
    team_stats[row.WTeamID]['or'] += row.WOR
    team_stats[row.LTeamID]['dr'] += row.LDR
    team_stats[row.WTeamID]['dr'] += row.WDR
    team_stats[row.LTeamID]['ast'] += row.LAst
    team_stats[row.WTeamID]['ast'] += row.WAst
    team_stats[row.LTeamID]['to'] += row.LTO
    team_stats[row.WTeamID]['to'] += row.WTO
    team_stats[row.LTeamID]['stl'] += row.LStl
    team_stats[row.WTeamID]['stl'] += row.WStl
    team_stats[row.LTeamID]['blk'] += row.LBlk
    team_stats[row.WTeamID]['blk'] += row.WBlk
    team_stats[row.LTeamID]['pf'] += row.LPF
    team_stats[row.WTeamID]['pf'] += row.WPF
    team_stats[row.LTeamID]['opp_points'] += row.WScore
    team_stats[row.WTeamID]['opp_points'] += row.LScore
    team_stats[row.LTeamID]['opp_fgm'] += row.WFGM
    team_stats[row.WTeamID]['opp_fgm'] += row.LFGM
    team_stats[row.LTeamID]['opp_fga'] += row.WFGA
    team_stats[row.WTeamID]['opp_fga'] += row.LFGA
    team_stats[row.LTeamID]['opp_fgm3'] += row.WFGM3
    team_stats[row.WTeamID]['opp_fgm3'] += row.LFGM3
    team_stats[row.LTeamID]['opp_fga3'] += row.WFGA3
    team_stats[row.WTeamID]['opp_fga3'] += row.LFGA3
    team_stats[row.LTeamID]['opp_fta'] += row.WFTA
    team_stats[row.WTeamID]['opp_fta'] += row.LFTA
    team_stats[row.LTeamID]['opp_ftm'] += row.WFTM
    team_stats[row.WTeamID]['opp_ftm'] += row.LFTM
    team_stats[row.LTeamID]['opp_or'] += row.WOR
    team_stats[row.WTeamID]['opp_or'] += row.LOR
    team_stats[row.LTeamID]['opp_dr'] += row.WDR
    team_stats[row.WTeamID]['opp_dr'] += row.LDR
    team_stats[row.LTeamID]['opp_ast'] += row.WAst
    team_stats[row.WTeamID]['opp_ast'] += row.LAst
    team_stats[row.LTeamID]['opp_to'] += row.WTO
    team_stats[row.WTeamID]['opp_to'] += row.LTO
    team_stats[row.LTeamID]['opp_stl'] += row.WStl
    team_stats[row.WTeamID]['opp_stl'] += row.LStl
    team_stats[row.LTeamID]['opp_blk'] += row.WBlk
    team_stats[row.WTeamID]['opp_blk'] += row.LBlk
    team_stats[row.LTeamID]['opp_pf'] += row.WPF
    team_stats[row.WTeamID]['opp_pf'] += row.LPF
    return team_stats, team_results, glicko

def make_row(team_stats, team_results, glicko, kenpom_matrix, id0, id1, year, tourny = -1, label = -1):
    row = {'year': year, 'label': label, 'tourny': tourny}

    #kenpom
    row['adj_off_eff_0'] = kenpom_matrix[kenpom_matrix['team_id'] == id0].adj_off_eff.values[0]
    row['adj_def_eff_0'] = kenpom_matrix[kenpom_matrix['team_id'] == id0].adj_def_eff.values[0]
    row['adj_eff_0'] = kenpom_matrix[kenpom_matrix['team_id'] == id0].adj_eff.values[0]
    row['seed_0'] = kenpom_matrix[kenpom_matrix['team_id'] == id0].seed.values[0]
    row['adj_off_eff_1'] = kenpom_matrix[kenpom_matrix['team_id'] == id1].adj_off_eff.values[0]
    row['adj_def_eff_1'] = kenpom_matrix[kenpom_matrix['team_id'] == id1].adj_def_eff.values[0]
    row['adj_eff_1'] = kenpom_matrix[kenpom_matrix['team_id'] == id1].adj_eff.values[0]
    row['seed_1'] = kenpom_matrix[kenpom_matrix['team_id'] == id1].seed.values[0]

    #glicko
    rating_0, rating_1 = glicko[id1].getRating(), glicko[id0].getRating()
    rd_0, rd_1 = glicko[id1].getRd(), glicko[id0].getRd()

    row['glicko_0'] = rating_0
    row['glicko_1'] = rating_1

    #RPI and win percentage
    #win percentage
    temp = 0
    for game in team_results[id0]:
        temp += game['result']
    if len(team_results[id0]) == 0:
        wp0 = 0
    else:
        wp0 = float(temp)/len(team_results[id0])
    row['win_rate_0'] = wp0

    temp = 0
    for game in team_results[id1]:
        temp += game['result']
    if len(team_results[id1]) == 0:
        wp1 = 0
    else:
        wp1 = float(temp)/len(team_results[id1])
    row['win_rate_1'] = wp1

    #weighted win percentage
    temp = 0.0
    for game in team_results[id0]:
        if game['loc'] == 'N':
            temp += 1*game['result']
        elif game['loc'] == 'H':
            temp += 1.4*game['result']
        else:
            temp += .6*game['result']
    if len(team_results[id0]) == 0:
        wwp0 = 0
    else:
        wwp0 = temp/len(team_results[id0])
    row['weighted_win_rate_0'] = wwp0

    temp = 0.0
    for game in team_results[id1]:
        if game['loc'] == 'N':
            temp += 1*game['result']
        elif game['loc'] == 'A':
            temp += 1.4*game['result']
        else:
            temp += .6*game['result']
    if len(team_results[id1]) == 0:
        wwp1 = 0
    else:
        wwp1 = temp/len(team_results[id1])
    row['weighted_win_rate_1'] = wwp1

    #Opponents win percentage
    temp = 0
    denom = 0.0
    for game in team_results[id0]:
        for game2 in team_results[game['opponent']]:
            if game2['opponent'] != id0:
                temp += game2['result']
                denom += 1
    if denom == 0:
        owp0 = 0
    else:
        owp0 = temp/denom
    row['opponents_win_rate_0'] = owp0

    temp = 0
    denom = 0.0
    for game in team_results[id1]:
        for game2 in team_results[game['opponent']]:
            if game2['opponent'] != id1:
                temp += game2['result']
                denom += 1
    if denom == 0:
        owp1 = 0
    else:
        owp1 = temp/denom
    row['opponents_win_rate_1'] = owp1

    #Opponents opponents win percentage
    temp = 0
    denom = 0.0
    for game in team_results[id0]:
        for game2 in team_results[game['opponent']]:
            for game3 in team_results[game2['opponent']]:
                if game3['opponent'] != id0:
                    temp += game3['result']
                    denom += 1
    if denom == 0:
        oowp0 = 0
    else:
        oowp0 = temp/denom
    row['opponents_opponents_win_rate_0'] = oowp0

    temp = 0
    denom = 0.0
    for game in team_results[id1]:
        for game2 in team_results[game['opponent']]:
            for game3 in team_results[game2['opponent']]:
                if game3['opponent'] != id1:
                    temp += game3['result']
                    denom += 1
    if denom == 0:
        oowp1 = 0
    else:
        oowp1 = temp/denom
    row['opponents_opponents_win_rate_1'] = oowp1

    row['rpi_0'] = .25*wwp0 + .5*owp0 + .25*oowp0
    row['rpi_1'] = .25*wwp1 + .5*owp1 + .25*oowp1

    #ids and labels
    row['id_0'] = id0
    row['id_1'] = id1

    if team_stats[id0]['games'] == 0:
        team_stats[id0]['games'] = -1
    if team_stats[id1]['games'] == 0:
        team_stats[id1]['games'] = -1

    row['points_0'] = team_stats[id0]['points']/team_stats[id0]['games']
    row['points_1'] = team_stats[id1]['points']/team_stats[id1]['games']
    row['fgm_0'] = team_stats[id0]['fgm']/team_stats[id0]['games']
    row['fgm_1'] = team_stats[id1]['fgm']/team_stats[id1]['games']
    row['fga_0'] = team_stats[id0]['fga']/team_stats[id0]['games']
    row['fga_1'] = team_stats[id1]['fga']/team_stats[id1]['games']
    row['fgm3_0'] = team_stats[id0]['fgm3']/team_stats[id0]['games']
    row['fgm3_1'] = team_stats[id1]['fgm3']/team_stats[id1]['games']
    row['fga3_0'] = team_stats[id0]['fga3']/team_stats[id0]['games']
    row['fga3_1'] = team_stats[id1]['fga3']/team_stats[id1]['games']
    row['fta_0'] = team_stats[id0]['fta']/team_stats[id0]['games']
    row['fta_1'] = team_stats[id1]['fta']/team_stats[id1]['games']
    row['ftm_0'] = team_stats[id0]['ftm']/team_stats[id0]['games']
    row['or_0'] = team_stats[id0]['or']/team_stats[id0]['games']
    row['ftm_1'] = team_stats[id1]['ftm']/team_stats[id1]['games']
    row['or_1'] = team_stats[id1]['or']/team_stats[id1]['games']
    row['dr_0'] = team_stats[id0]['dr']/team_stats[id0]['games']
    row['dr_1'] = team_stats[id1]['dr']/team_stats[id1]['games']
    row['ast_0'] = team_stats[id0]['ast']/team_stats[id0]['games']
    row['ast_1'] = team_stats[id1]['ast']/team_stats[id1]['games']
    row['to_0'] = team_stats[id0]['to']/team_stats[id0]['games']
    row['to_1'] = team_stats[id1]['to']/team_stats[id1]['games']
    row['stl_0'] = team_stats[id0]['stl']/team_stats[id0]['games']
    row['stl_1'] = team_stats[id1]['stl']/team_stats[id1]['games']
    row['blk_0'] = team_stats[id0]['blk']/team_stats[id0]['games']
    row['blk_1'] = team_stats[id1]['blk']/team_stats[id1]['games']
    row['pf_0'] = team_stats[id0]['pf']/team_stats[id0]['games']
    row['pf_1'] = team_stats[id1]['pf']/team_stats[id1]['games']
    row['opp_points_0'] = team_stats[id0]['opp_points']/team_stats[id0]['games']
    row['opp_points_1'] = team_stats[id1]['opp_points']/team_stats[id1]['games']
    row['opp_fgm_0'] = team_stats[id0]['opp_fgm']/team_stats[id0]['games']
    row['opp_fgm_1'] = team_stats[id1]['opp_fgm']/team_stats[id1]['games']
    row['opp_fga_0'] = team_stats[id0]['opp_fga']/team_stats[id0]['games']
    row['opp_fga_1'] = team_stats[id1]['opp_fga']/team_stats[id1]['games']
    row['opp_fgm3_0'] = team_stats[id0]['opp_fgm3']/team_stats[id0]['games']
    row['opp_fgm3_1'] = team_stats[id1]['opp_fgm3']/team_stats[id1]['games']
    row['opp_fga3_0'] = team_stats[id0]['opp_fga3']/team_stats[id0]['games']
    row['opp_fga3_1'] = team_stats[id1]['opp_fga3']/team_stats[id1]['games']
    row['opp_fta_0'] = team_stats[id0]['opp_fta']/team_stats[id0]['games']
    row['opp_fta_1'] = team_stats[id1]['opp_fta']/team_stats[id1]['games']
    row['opp_ftm_0'] = team_stats[id0]['opp_ftm']/team_stats[id0]['games']
    row['opp_or_0'] = team_stats[id0]['opp_or']/team_stats[id0]['games']
    row['opp_ftm_1'] = team_stats[id1]['opp_ftm']/team_stats[id1]['games']
    row['opp_or_1'] = team_stats[id1]['opp_or']/team_stats[id1]['games']
    row['opp_dr_0'] = team_stats[id0]['opp_dr']/team_stats[id0]['games']
    row['opp_dr_1'] = team_stats[id1]['opp_dr']/team_stats[id1]['games']
    row['opp_ast_0'] = team_stats[id0]['opp_ast']/team_stats[id0]['games']
    row['opp_ast_1'] = team_stats[id1]['opp_ast']/team_stats[id1]['games']
    row['opp_to_0'] = team_stats[id0]['opp_to']/team_stats[id0]['games']
    row['opp_to_1'] = team_stats[id1]['opp_to']/team_stats[id1]['games']
    row['opp_stl_0'] = team_stats[id0]['opp_stl']/team_stats[id0]['games']
    row['opp_stl_1'] = team_stats[id1]['opp_stl']/team_stats[id1]['games']
    row['opp_blk_0'] = team_stats[id0]['opp_blk']/team_stats[id0]['games']
    row['opp_blk_1'] = team_stats[id1]['opp_blk']/team_stats[id1]['games']
    row['opp_pf_0'] = team_stats[id0]['opp_pf']/team_stats[id0]['games']
    row['opp_pf_1'] = team_stats[id1]['opp_pf']/team_stats[id1]['games']

    #possesions and offensive/defensive defensive efficiencies
    row['poss_0'] = team_stats[id0]['possesions']/team_stats[id0]['games']
    row['poss_1'] = team_stats[id1]['possesions']/team_stats[id1]['games']

    if team_stats[id0]['games'] == -1:
        team_stats[id0]['games'] = 0
    if team_stats[id1]['games'] == -1:
        team_stats[id1]['games'] = 0

    if team_stats[id0]['possesions'] == 0:
        team_stats[id0]['possesions'] = -1
    if team_stats[id1]['possesions'] == 0:
        team_stats[id1]['possesions'] = -1

    row['def_eff_0'] = team_stats[id0]['opp_points']/team_stats[id0]['possesions']*100.0
    row['def_eff_1'] = team_stats[id1]['opp_points']/team_stats[id1]['possesions']*100.0
    row['off_eff_0'] = team_stats[id0]['points']/team_stats[id0]['possesions']*100.0
    row['off_eff_1'] = team_stats[id1]['points']/team_stats[id1]['possesions']*100.0

    if team_stats[id0]['possesions'] == -1:
        team_stats[id0]['possesions'] = 0
    if team_stats[id1]['possesions'] == -1:
        team_stats[id1]['possesions'] = 0

    #Pythagorean expectation
    if team_stats[id0]['points'] == 0:
        row['pyth_exp_0'] = 0
    else:
        row['pyth_exp_0'] = 1.0/(1 + (team_stats[id0]['opp_points']*1.0/team_stats[id0]['points'])**8)
    if team_stats[id1]['points'] == 0:
        row['pyth_exp_1'] = 0
    else:
        row['pyth_exp_1'] = 1.0/(1 + (team_stats[id1]['opp_points']*1.0/team_stats[id1]['points'])**8)


    row = pd.DataFrame(row, index=[0])
    cols = ['tourny', 'year', 'id_0', 'id_1', 'ftm_0', 'fta_0', 'fgm_0', 'fga_0', 'fgm3_0', 'fga3_0', 'ast_0', 'blk_0', 'or_0', 'dr_0', 'stl_0', 'to_0', 'pf_0', 'points_0', 'poss_0', 'opp_ftm_0', 'opp_fta_0', 'opp_fgm_0', 'opp_fga_0', 'opp_fgm3_0', 'opp_fga3_0', 'opp_ast_0', 'opp_blk_0', 'opp_or_0', 'opp_dr_0', 'opp_stl_0', 'opp_to_0', 'opp_pf_0', 'opp_points_0', 'pyth_exp_0', 'win_rate_0', 'opponents_win_rate_0', 'opponents_opponents_win_rate_0', 'weighted_win_rate_0', 'rpi_0', 'off_eff_0', 'def_eff_0', 'glicko_0', 'ftm_1', 'fta_1', 'fgm_1', 'fga_1', 'fgm3_1', 'fga3_1', 'ast_1', 'blk_1', 'or_1', 'dr_1', 'stl_1', 'to_1', 'pf_1', 'points_1', 'poss_1', 'opp_ftm_1', 'opp_fta_1', 'opp_fgm_1', 'opp_fga_1', 'opp_fgm3_1', 'opp_fga3_1', 'opp_ast_1', 'opp_blk_1', 'opp_or_1', 'opp_dr_1', 'opp_stl_1', 'opp_to_1', 'opp_pf_1', 'opp_points_1', 'pyth_exp_1', 'win_rate_1', 'opponents_win_rate_1', 'opponents_opponents_win_rate_1', 'weighted_win_rate_1', 'rpi_1', 'off_eff_1', 'def_eff_1', 'glicko_1', 'label']
    row = row[cols]
    return row

def generate_stats(id, team_stats, team_results, glicko, kenpom_matrix):
    row = {}

    #kenpom
    row['adj_off_eff'] = kenpom_matrix[kenpom_matrix['team_id'] == id].adj_off_eff.values[0]
    row['adj_def_eff'] = kenpom_matrix[kenpom_matrix['team_id'] == id].adj_def_eff.values[0]
    row['adj_eff'] = kenpom_matrix[kenpom_matrix['team_id'] == id].adj_eff.values[0]
    row['seed'] = kenpom_matrix[kenpom_matrix['team_id'] == id].seed.values[0]
    
    #glicko
    rating = glicko[id].getRating()
    row['glicko'] = rating

    #RPI and win percentage
    #win percentage
    temp = 0
    for game in team_results[id]:
        temp += game['result']
    if len(team_results[id]) == 0:
        wp0 = 0
    else:
        wp0 = float(temp)/len(team_results[id])
    row['win_rate'] = wp0

    #weighted win percentage
    temp = 0.0
    for game in team_results[id]:
        if game['loc'] == 'N':
            temp += 1*game['result']
        elif game['loc'] == 'H':
            temp += 1.4*game['result']
        else:
            temp += .6*game['result']
    if len(team_results[id]) == 0:
        wwp0 = 0
    else:
        wwp0 = temp/len(team_results[id])
    row['weighted_win_rate'] = wwp0

    #Opponents win percentage
    temp = 0
    denom = 0.0
    for game in team_results[id]:
        for game2 in team_results[game['opponent']]:
            if game2['opponent'] != id:
                temp += game2['result']
                denom += 1
    if denom == 0:
        owp0 = 0
    else:
        owp0 = temp/denom
    row['opponents_win_rate'] = owp0

    #Opponents opponents win percentage
    temp = 0
    denom = 0.0
    for game in team_results[id]:
        for game2 in team_results[game['opponent']]:
            for game3 in team_results[game2['opponent']]:
                if game3['opponent'] != id:
                    temp += game3['result']
                    denom += 1
    if denom == 0:
        oowp0 = 0
    else:
        oowp0 = temp/denom
    row['opponents_opponents_win_rate'] = oowp0

    row['rpi'] = .25*wwp0 + .5*owp0 + .25*oowp0

    #ids and labels
    row['id'] = id

    if team_stats[id]['games'] == 0:
        team_stats[id]['games'] = -1

    row['points'] = team_stats[id]['points']/team_stats[id]['games']
    row['fgm'] = team_stats[id]['fgm']/team_stats[id]['games']
    row['fga'] = team_stats[id]['fga']/team_stats[id]['games']
    row['fgm3'] = team_stats[id]['fgm3']/team_stats[id]['games']
    row['fga3'] = team_stats[id]['fga3']/team_stats[id]['games']
    row['fta'] = team_stats[id]['fta']/team_stats[id]['games']
    row['ftm'] = team_stats[id]['ftm']/team_stats[id]['games']
    row['or'] = team_stats[id]['or']/team_stats[id]['games']
    row['dr'] = team_stats[id]['dr']/team_stats[id]['games']
    row['ast'] = team_stats[id]['ast']/team_stats[id]['games']
    row['to'] = team_stats[id]['to']/team_stats[id]['games']
    row['stl'] = team_stats[id]['stl']/team_stats[id]['games']
    row['blk'] = team_stats[id]['blk']/team_stats[id]['games']
    row['pf'] = team_stats[id]['pf']/team_stats[id]['games']
    row['opp_points'] = team_stats[id]['opp_points']/team_stats[id]['games']
    row['opp_fgm'] = team_stats[id]['opp_fgm']/team_stats[id]['games']
    row['opp_fga'] = team_stats[id]['opp_fga']/team_stats[id]['games']
    row['opp_fgm3'] = team_stats[id]['opp_fgm3']/team_stats[id]['games']
    row['opp_fga3'] = team_stats[id]['opp_fga3']/team_stats[id]['games']
    row['opp_fta'] = team_stats[id]['opp_fta']/team_stats[id]['games']
    row['opp_ftm'] = team_stats[id]['opp_ftm']/team_stats[id]['games']
    row['opp_or'] = team_stats[id]['opp_or']/team_stats[id]['games']
    row['opp_dr'] = team_stats[id]['opp_dr']/team_stats[id]['games']
    row['opp_ast'] = team_stats[id]['opp_ast']/team_stats[id]['games']
    row['opp_to'] = team_stats[id]['opp_to']/team_stats[id]['games']
    row['opp_stl'] = team_stats[id]['opp_stl']/team_stats[id]['games']
    row['opp_blk'] = team_stats[id]['opp_blk']/team_stats[id]['games']
    row['opp_pf'] = team_stats[id]['opp_pf']/team_stats[id]['games']

    #possesions and offensive/defensive defensive efficiencies
    row['poss'] = team_stats[id]['possesions']/team_stats[id]['games']

    if team_stats[id]['games'] == -1:
        team_stats[id]['games'] = 0
   
    if team_stats[id]['possesions'] == 0:
        team_stats[id]['possesions'] = -1

    row['def_eff'] = team_stats[id]['opp_points']/team_stats[id]['possesions']*100.0
    row['off_eff'] = team_stats[id]['points']/team_stats[id]['possesions']*100.0

    if team_stats[id]['possesions'] == -1:
        team_stats[id]['possesions'] = 0
    
    #Pythagorean expectation
    if team_stats[id]['points'] == 0:
        row['pyth_exp'] = 0
    else:
        row['pyth_exp'] = 1.0/(1 + (team_stats[id]['opp_points']*1.0/team_stats[id]['points'])**8)

    #row = pd.DataFrame(row, index=[0])
    #cols = ['id', 'ftm', 'fta', 'fgm', 'fga', 'fgm3', 'fga3', 'ast', 'blk', 'or', 'dr', 'stl', 'to', 'pf', 'points', 'poss', 'opp_ftm', 'opp_fta', 'opp_fgm', 'opp_fga', 'opp_fgm3', 'opp_fga3', 'opp_ast', 'opp_blk', 'opp_or', 'opp_dr', 'opp_stl', 'opp_to', 'opp_pf', 'opp_points', 'pyth_exp', 'win_rate', 'opponents_win_rate', 'opponents_opponents_win_rate', 'weighted_win_rate', 'rpi', 'off_eff', 'def_eff', 'glicko']
    #row = row[cols]
    return row


def getDataMatrix(year):
    df_reg_season = pd.read_csv(KAGGLE_RAW_PATH+'RegularSeasonDetailedResults.csv')
    df_reg_season['tourny'] = 0
    df_ncaa_tourny = pd.read_csv(KAGGLE_RAW_PATH+'NCAATourneyDetailedResults.csv')
    df_ncaa_tourny['tourny'] = 1
    df_reg_season.sort_values(by=['Season','DayNum'])
    df_reg_season = df_reg_season.loc[df_reg_season['Season'].isin([year])]
    df_ncaa_tourny.sort_values(by=['Season','DayNum'])
    df_ncaa_tourny = df_ncaa_tourny.loc[df_ncaa_tourny['Season'].isin([year])]

    team_ids = set(df_reg_season.WTeamID).union(set(df_reg_season.LTeamID))
    glicko = dict(zip(list(team_ids), [Player() for _ in range(len(team_ids))]))
    kenpom_matrix = pd.read_csv(KENPOM_PROCESSED_PATH+"{}kenpom_processed.csv".format(year))
    team_results = {}
    team_stats = {}
    tournament_stats = {}
    for id in team_ids:
        team_results[id] = []
        team_stats[id] = {'games': 0.0, 'points': 0.0, 'fgm': 0.0, 'fga': 0.0, 'fgm3': 0.0, 'fga3': 0.0, 'ftm': 0.0, 'fta': 0.0, 'or': 0.0, 'dr': 0.0, 'to': 0.0, 'ast': 0.0, 'stl': 0.0, 'blk': 0.0, 'pf': 0.0,'opp_points': 0.0, 'opp_fgm': 0.0, 'opp_fga': 0.0, 'opp_fgm3': 0.0, 'opp_fga3': 0.0, 'opp_ftm': 0.0, 'opp_fta': 0.0, 'opp_or': 0.0, 'opp_dr': 0.0, 'opp_to': 0.0, 'opp_ast': 0.0, 'opp_stl': 0.0, 'opp_blk': 0.0, 'opp_pf': 0.0, 'possesions': 0.0, 'adj_off_eff': 0.0, 'adj_def_eff': 0.0, 'adj_eff': 0.0, 'seed': 0}

    data_matrix = pd.DataFrame()

    for row in df_reg_season.itertuples():
        team_stats, team_results, glicko = update_stats(team_stats, team_results, glicko, kenpom_matrix, row)

    for team in team_ids:
        #Update kenpom rankings
        try:
            team_stats[team]['adj_off_eff'] = kenpom_matrix[kenpom_matrix['team_id'] == team].adj_off_eff.values[0]
            team_stats[team]['adj_def_eff'] = kenpom_matrix[kenpom_matrix['team_id'] == team].adj_def_eff.values[0]
            team_stats[team]['adj_eff'] = kenpom_matrix[kenpom_matrix['team_id'] == team].adj_eff.values[0]
            team_stats[team]['seed'] = kenpom_matrix[kenpom_matrix['team_id'] == team].seed.values[0]
        except:
            # A few teams (~5 throughout all years) are not in the kenpom dataset for some seasons
            # These are always small schools that dont make the tournament, so we can just leave these rows as blank
            pass

    for row in df_ncaa_tourny.itertuples():
        data_matrix = data_matrix.append(make_row(team_stats, team_results, glicko, kenpom_matrix, min(row.WTeamID, row.LTeamID), max(row.WTeamID, row.LTeamID), row.Season, row.tourny, 1 if row.WTeamID > row.LTeamID else 0))
        id0 = min(row.WTeamID, row.LTeamID)
        id1 = max(row.WTeamID, row.LTeamID)
        tournament_stats[id0] = generate_stats(id0,team_stats, team_results, glicko, kenpom_matrix)
        tournament_stats[id1] = generate_stats(id1,team_stats, team_results, glicko, kenpom_matrix)
    
    tournament_stats_df = pd.DataFrame(tournament_stats)
    team_stats = pd.DataFrame(team_stats)

    return data_matrix, team_stats, tournament_stats_df

if __name__ == "__main__":
    for year in range(2003,2018):
        data_matrix, team_stats, tournament_stats = getDataMatrix(year)
        data_matrix.to_csv(TOURNAMENT_MATRICES_PATH+'{}dataMatrix.csv'.format(year))
        print('Created file {}dataMatrix.csv'.format(year))
        team_stats.to_csv(TEAM_STATS_PATH+'{}teamStats.csv'.format(year))
        print('Created file {}teamStats.csv'.format(year))
        tournament_stats.to_csv(TOURNAMENT_STATS_PATH+'{}tournamentStats.csv'.format(year))
        print('Created file {}tournamentStats.csv'.format(year))

